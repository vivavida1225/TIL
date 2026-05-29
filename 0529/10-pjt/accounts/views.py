import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import PreferenceChoice, UserPreference

User = get_user_model()

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/login.html')

def kakao_login(request):
    client_id = settings.KAKAO_REST_API_KEY
    redirect_uri = settings.KAKAO_REDIRECT_URI
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_auth_url)

def kakao_callback(request):
    code = request.GET.get('code')
    if not code:
        messages.error(request, "카카오 로그인 인증 코드를 받지 못했습니다.")
        return redirect('accounts:login')

    client_id = settings.KAKAO_REST_API_KEY
    client_secret = settings.KAKAO_LOGIN_CLIENT_SECRET
    redirect_uri = settings.KAKAO_REDIRECT_URI

    # 1. Access Token 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    try:
        token_response = requests.post(token_url, headers=headers, data=data)
        token_json = token_response.json()
        
        if 'error' in token_json:
            messages.error(request, f"토큰 발급 실패: {token_json.get('error_description')}")
            return redirect('accounts:login')
            
        access_token = token_json.get('access_token')
    except Exception as e:
        messages.error(request, f"카카오 서버 통신 중 오류가 발생했습니다: {str(e)}")
        return redirect('accounts:login')

    # 2. 사용자 정보 요청
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    user_info_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    try:
        user_info_response = requests.get(user_info_url, headers=user_info_headers)
        user_info_json = user_info_response.json()
        
        if 'id' not in user_info_json:
            messages.error(request, "사용자 정보를 가져오지 못했습니다.")
            return redirect('accounts:login')
            
        kakao_id = str(user_info_json.get('id'))
    except Exception as e:
        messages.error(request, f"카카오 사용자 정보 요청 중 오류 발생: {str(e)}")
        return redirect('accounts:login')

    # 3. 로그인 또는 회원가입 처리
    kakao_account = user_info_json.get('kakao_account', {})
    profile = kakao_account.get('profile', {})
    properties = user_info_json.get('properties', {})
    
    email = kakao_account.get('email', '')
    nickname = profile.get('nickname') or properties.get('nickname') or f"KakaoUser_{kakao_id[:5]}"
    profile_image_url = profile.get('profile_image_url') or properties.get('profile_image') or ''

    try:
        user = User.objects.get(kakao_id=kakao_id)
        # 프로필 이미지나 닉네임이 바뀌었다면 업데이트
        updated = False
        if profile_image_url and user.profile_image_url != profile_image_url:
            user.profile_image_url = profile_image_url
            updated = True
        if nickname and user.first_name != nickname:
            user.first_name = nickname
            updated = True
        if updated:
            user.save()
    except User.DoesNotExist:
        # 카카오 id 로 등록된 유저가 없다면 새로 가입 처리
        username = f"kakao_{kakao_id}"
        
        if User.objects.filter(username=username).exists():
            username = f"kakao_{kakao_id}_{User.objects.count()}"

        user = User.objects.create_user(
            username=username,
            email=email,
            kakao_id=kakao_id,
            first_name=nickname,
            profile_image_url=profile_image_url
        )
        user.set_unusable_password()
        user.save()

    # 로그인 세션 처리
    auth_login(request, user)
    messages.success(request, f"{user.first_name or user.username}님, 환영합니다!")
    return redirect('home')

def logout(request):
    auth_logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect('home')

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['travels'] = request.user.travels.prefetch_related('countries', 'cities').all()
    return render(request, 'index.html', context)

@login_required
def additional_info(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        birth_date_str = request.POST.get('birth_date')
        
        # 필수 값 검증
        if not nickname or not gender or not birth_date_str:
            messages.error(request, "닉네임, 성별, 생년월일은 모두 필수 입력 항목입니다.")
            return render(request, 'accounts/additional_info.html', {
                'error': '모든 필수 항목을 입력해주세요.'
            })
            
        # 닉네임 중복 검사
        nickname = nickname.strip()
        if User.objects.filter(nickname=nickname).exclude(id=request.user.id).exists():
            messages.error(request, "이미 사용 중인 닉네임입니다. 다른 닉네임을 입력해 주세요.")
            return render(request, 'accounts/additional_info.html', {
                'error': '이미 사용 중인 닉네임입니다.'
            })
            
        user = request.user
        user.nickname = nickname
        user.first_name = nickname # 통합 사용을 위해 first_name에도 동기화
        user.gender = gender
        user.birth_date = birth_date_str
        user.save()
        
        messages.success(request, "추가 프로필 정보가 안전하게 저장되었습니다!")
        return redirect('accounts:preference_step', step_num=1)
        
    return render(request, 'accounts/additional_info.html')

def seed_choices_if_empty():
    if PreferenceChoice.objects.count() == 0:
        styles = [
            ('style_food', 'STYLE', '맛집 선호'),
            ('style_sight', 'STYLE', '관광지 선호 (긴바지, 스카프 등 대비 필요)'),
            ('style_museum', 'STYLE', '박물관 미술관 선호 (유선이어폰)'),
            ('style_activity', 'STYLE', '액티비티 선호 (수영, 트래킹 등)'),
            ('style_souvenir', 'STYLE', '기념품 수집 선호'),
            ('style_walk_lot', 'STYLE', '많이 걸어다녀도 좋아요'),
            ('style_no_walk', 'STYLE', '다리 아픈건 싫어요'),
            ('style_cost_eff', 'STYLE', '귀찮아도 가성비'),
            ('style_comfort', 'STYLE', '돈 좀 쓰고 편하게'),
            ('style_bring_all', 'STYLE', '다 챙겨간다'),
            ('style_buy_local', 'STYLE', '필요한거 생기면 현지 조달한다'),
        ]
        tastes = [
            ('taste_korean', 'TASTE', '죽어도 한식'),
            ('taste_greasy', 'TASTE', '느끼해도 괜찮다'),
            ('taste_spices', 'TASTE', '향신료(고수 등) 괜찮다'),
            ('taste_sweet_salty', 'TASTE', '짜다/달다'),
            ('taste_authentic', 'TASTE', '찐 로컬 음식 좋다'),
        ]
        for key, cat, name in styles + tastes:
            PreferenceChoice.objects.get_or_create(key=key, category=cat, defaults={'name': name})

@login_required
def preference_step(request, step_num):
    if step_num < 1 or step_num > 4:
        return redirect('home')
        
    seed_choices_if_empty()
    user_pref, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # "다음에 입력하기" (스킵) 처리
        if 'skip' in request.POST:
            if step_num == 4:
                messages.success(request, "추가 설정을 나중에 입력하기로 하셨습니다. 플래닝을 즐겨보세요!")
                return redirect('home')
            return redirect('accounts:preference_step', step_num=step_num + 1)
            
        # 단계별 데이터 저장
        if step_num == 1:
            hygiene = request.POST.get('hygiene_sensitivity')
            if hygiene:
                user_pref.hygiene_sensitivity = int(hygiene)
                user_pref.save()
        elif step_num == 2:
            preparedness = request.POST.get('preparedness')
            if preparedness:
                user_pref.preparedness = int(preparedness)
                user_pref.save()
        elif step_num == 3:
            selected_ids = request.POST.getlist('style_choices')
            user_pref.choices.remove(*user_pref.choices.filter(category='STYLE'))
            user_pref.choices.add(*PreferenceChoice.objects.filter(id__in=selected_ids, category='STYLE'))
        elif step_num == 4:
            selected_ids = request.POST.getlist('taste_choices')
            user_pref.choices.remove(*user_pref.choices.filter(category='TASTE'))
            user_pref.choices.add(*PreferenceChoice.objects.filter(id__in=selected_ids, category='TASTE'))
            
            messages.success(request, "모든 맞춤형 여행 취향 연동이 완료되었습니다!")
            return redirect('home')
            
        return redirect('accounts:preference_step', step_num=step_num + 1)
        
    # GET: 단계별 템플릿 전달
    context = {
        'step_num': step_num, 
        'user_pref': user_pref
    }
    if step_num == 3:
        context['choices'] = PreferenceChoice.objects.filter(category='STYLE')
    elif step_num == 4:
        context['choices'] = PreferenceChoice.objects.filter(category='TASTE')
        
    return render(request, f'accounts/preference_step_{step_num}.html', context)

from django.shortcuts import get_object_or_404

def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    travels = target_user.travels.prefetch_related('countries', 'cities').all()
    preference = getattr(target_user, 'preference', None)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.followings.filter(id=target_user.id).exists()
        
    followers_count = target_user.followers.count()
    followings_count = target_user.followings.count()
    
    context = {
        'target_user': target_user,
        'travels': travels,
        'preference': preference,
        'is_following': is_following,
        'followers_count': followers_count,
        'followings_count': followings_count,
    }
    return render(request, 'accounts/user_profile.html', context)

@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user == target_user:
        messages.error(request, "자기 자신을 팔로우할 수는 없습니다.")
        return redirect('accounts:user_profile', user_id=user_id)
        
    if request.user.followings.filter(id=target_user.id).exists():
        request.user.followings.remove(target_user)
        messages.success(request, f"{target_user.nickname or target_user.first_name}님을 언팔로우했습니다.")
    else:
        request.user.followings.add(target_user)
        messages.success(request, f"{target_user.nickname or target_user.first_name}님을 팔로우합니다!")
        
    return redirect('accounts:user_profile', user_id=user_id)
