from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from travel.models import Travel

def post_list(request):
    posts = Post.objects.select_related('user', 'travel').prefetch_related(
        'travel__countries', 'travel__cities', 'likes', 'scraps'
    ).all()
    context = {
        'posts': posts
    }
    return render(request, 'community/post_list.html', context)

@login_required
def post_create(request):
    user = request.user
    # 공유를 시도하기 전에 사용자가 최소 1개 이상의 여행 일정을 가지고 있는지 체크
    user_travels = user.travels.prefetch_related('countries', 'cities').all()
    if not user_travels.exists():
        messages.warning(request, "공유할 수 있는 여행 일정이 아직 없습니다. 대시보드에서 여행 준비를 먼저 시작해 주세요!")
        return redirect('home')
        
    if request.method == 'POST':
        travel_id = request.POST.get('travel')
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if not travel_id or not title or not content:
            messages.error(request, "제목, 내용 및 공유할 여행 일정은 모두 필수 기입 항목입니다.")
            return redirect('community:post_create')
            
        travel = get_object_or_404(Travel, id=travel_id)
        if travel.user != user:
            messages.error(request, "자신의 여행 일정만 공유할 수 있습니다.")
            return redirect('community:post_create')
            
        post = Post.objects.create(
            user=user,
            travel=travel,
            title=title,
            content=content
        )
        messages.success(request, "새로운 여행 플랜 공유글이 성황리에 등록되었습니다!")
        return redirect('community:post_list')
        
    context = {
        'travels': user_travels
    }
    return render(request, 'community/post_create.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('user', 'travel').prefetch_related(
        'travel__countries', 'travel__cities', 'likes', 'scraps'
    ), id=post_id)
    
    comments = post.comments.select_related('user').all()
    
    is_liked = False
    is_scraped = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(id=request.user.id).exists()
        is_scraped = post.scraps.filter(id=request.user.id).exists()
        
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'is_scraped': is_scraped,
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    liked = False
    
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')
    
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        if not is_ajax:
            messages.success(request, "이 공유글의 좋아요를 취소했습니다.")
    else:
        post.likes.add(user)
        liked = True
        if not is_ajax:
            messages.success(request, "이 공유글에 좋아요를 보냈습니다! ❤️")
            
    if is_ajax:
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
        
    return redirect('community:post_detail', post_id=post_id)

@login_required
def post_scrap(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    scraped = False
    
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')
    
    if post.scraps.filter(id=user.id).exists():
        post.scraps.remove(user)
        if not is_ajax:
            messages.success(request, "이 공유글 스크랩을 보류했습니다.")
    else:
        post.scraps.add(user)
        scraped = True
        if not is_ajax:
            messages.success(request, "이 공유글을 보관함에 스크랩했습니다! ⭐")
            
    if is_ajax:
        return JsonResponse({
            'scraped': scraped,
            'scraps_count': post.scraps.count()
        })
        
    return redirect('community:post_detail', post_id=post_id)

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if not content or not content.strip():
            messages.error(request, "댓글 내용은 한 글자 이상 기입해 주셔야 합니다.")
            return redirect('community:post_detail', post_id=post_id)
            
        Comment.objects.create(
            post=post,
            user=request.user,
            content=content.strip()
        )
        messages.success(request, "댓글이 성공적으로 등록되었습니다.")
        
    return redirect('community:post_detail', post_id=post_id)

@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, "댓글을 삭제할 수 있는 권한이 없습니다.")
        return redirect('community:post_detail', post_id=post_id)
        
    comment.delete()
    messages.success(request, "댓글이 안전하게 삭제되었습니다.")
    return redirect('community:post_detail', post_id=post_id)
