from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Country, City, Travel
from .helpers import seed_travel_countries_and_cities
import json


def _get_season(month):
    if month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    elif month in [9, 10, 11]:
        return '가을'
    else:
        return '겨울'


def _build_search_queries(cities, countries, season):
    queries = []
    for city in cities[:2]:
        queries.append(f"{city} {season} 여행")
    for city in cities[:2]:
        queries.append(f"{city} 관광지 볼거리")
    for country in countries[:2]:
        queries.append(f"{country} 여행 추천")
    if cities:
        queries.append(f"{cities[0]} 맛집")
    if countries:
        queries.append(f"{countries[0]} {season} 날씨 준비물")
    return queries

@login_required
def create_travel(request):
    # 1. 온보딩 상태 검증 (기본 인적사항성별, 생년월일이 필수 입력되었는지 확인)
    user = request.user
    if not user.gender or not user.birth_date:
        messages.error(request, "여행 등록에 앞서서, 사용자 기본 프로필 정보 입력이 필요합니다.")
        return redirect('accounts:additional_info')
        
    # 2. 국가 및 도시 데이터 자동 시딩
    seed_travel_countries_and_cities()
    
    if request.method == 'POST':
        selected_country_ids = request.POST.getlist('countries')
        selected_city_ids = request.POST.getlist('cities')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # 유효성 검증
        if not selected_country_ids:
            messages.error(request, "최소 한 개 이상의 국가를 선택해야 합니다.")
            return redirect('travel:create_travel')
        if not selected_city_ids:
            messages.error(request, "최소 한 개 이상의 도시를 선택해야 합니다.")
            return redirect('travel:create_travel')
        if not start_date or not end_date:
            messages.error(request, "여행 기간을 입력해 주세요.")
            return redirect('travel:create_travel')
        if start_date > end_date:
            messages.error(request, "출발일은 도착일보다 늦을 수 없습니다.")
            return redirect('travel:create_travel')
            
        try:
            # 3. 여행 정보 저장
            travel = Travel.objects.create(
                user=user,
                start_date=start_date,
                end_date=end_date
            )
            # 관계 매핑 추가
            travel.countries.add(*Country.objects.filter(id__in=selected_country_ids))
            travel.cities.add(*City.objects.filter(id__in=selected_city_ids))
            travel.save()
            
            messages.success(request, "새로운 여행 일정이 성공적으로 등록되었습니다!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"저장 중 예기치 못한 오류가 발생했습니다: {str(e)}")
            return redirect('travel:create_travel')

    # GET 요청: 모든 국가와 하위 도시 정보를 쿼리하여 전달
    countries = Country.objects.prefetch_related('cities').all()
    
    # JavaScript에서 유기적 필터링을 쉽게 처리할 수 있도록 
    # 국가ID별 소속 도시의 {id, name} 목록을 JSON 문자열로 변환하여 템플릿에 주입
    country_city_map = {}
    for country in countries:
        country_city_map[country.id] = [
            {'id': city.id, 'name': city.name} for city in country.cities.all()
        ]
        
    context = {
        'countries': countries,
        'country_city_map_json': json.dumps(country_city_map, ensure_ascii=False)
    }
    return render(request, 'travel/create_travel.html', context)

@login_required
def travel_videos(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    countries = list(travel.countries.values_list('name', flat=True))
    cities = list(travel.cities.values_list('name', flat=True))
    season = _get_season(travel.start_date.month)
    queries = _build_search_queries(cities, countries, season)

    context = {
        'travel': travel,
        'countries': countries,
        'cities': cities,
        'season': season,
        'search_queries_json': json.dumps(queries, ensure_ascii=False),
        'countries_json': json.dumps(countries, ensure_ascii=False),
        'cities_json': json.dumps(cities, ensure_ascii=False),
        'youtube_api_key': settings.YOUTUBE_API_KEY,
    }
    return render(request, 'travel/travel_videos.html', context)


@login_required
def video_detail(request, video_id):
    context = {
        'video_id': video_id,
        'youtube_api_key': settings.YOUTUBE_API_KEY,
    }
    return render(request, 'travel/video_detail.html', context)


@login_required
def saved_videos(request):
    return render(request, 'travel/saved_videos.html')


@login_required
def saved_channels(request):
    return render(request, 'travel/saved_channels.html')


@login_required
def delete_travel(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    
    # 본인의 여행인지 유효성 검증
    if travel.user != request.user:
        messages.error(request, "해당 여행 일정을 삭제할 권한이 없습니다.")
        return redirect('home')
        
    travel.delete()
    messages.success(request, "여행 일정이 안전하게 삭제되었습니다.")
    return redirect('home')
