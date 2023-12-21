from django.shortcuts import render, redirect
from django.db.models import Count
from interactions.models import Post, Like, Save, Comment
from profiles.models import Profile
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def home(request):

    user_profile = Profile.objects.get(user=request.user)
    profiles = user_profile.follows.all()

    posts_with_like_counts = Post.objects.annotate(like_count=Count('post_likes')).order_by('-created_at')

    liked_posts = Like.objects.filter(user=request.user).values_list('post__id', flat=True)
    saved_posts = Save.objects.filter(user=request.user).values_list('post__id', flat=True)

    return render(request, 'home.html', {
        'profiles': profiles,
        'posts': posts_with_like_counts,
        'liked_posts': liked_posts,
        'saved_posts': saved_posts,
    })
    
@login_required(login_url='signin')
def post_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments_list = Comment.objects.filter(post=post).order_by('-created_at')  

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            new_comment = Comment.objects.create(author=request.user, post=post, text=text)  
            new_comment.save()
            return redirect('post_comments', pk=pk)

    paginator = Paginator(comments_list, 10)
    page = request.GET.get('page')

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'post_comments.html', {'post': post, 'comments': comments})