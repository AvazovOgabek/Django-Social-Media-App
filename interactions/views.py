from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Save, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required(login_url='signin')
def create_post_view(request):
    if request.method == 'POST':
        body = request.POST.get('body')
        post_img = request.FILES.get('post_img') if 'post_img' in request.FILES else None

        if body: 
            new_post = Post.objects.create(author=request.user, body=body, post_img=post_img)
            new_post.save()

            return redirect('home')

    return render(request, 'create_post.html')

@login_required(login_url='signin')
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    like = Like.objects.create(user=request.user, post=post)
    like.save()
    return redirect('home')

@login_required(login_url='signin')
def unlike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    like = Like.objects.get(user=request.user, post=post)
    like.delete()
    
    return redirect('home')

@login_required(login_url='signin')
def unsave_post(request, post_id): 
    post = Post.objects.get(pk=post_id)
    save = Save.objects.get(user=request.user, post=post)
    save.delete()
    return redirect('home')

@login_required(login_url='signin')
def save_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    save = Save.objects.create(user=request.user, post=post)
    save.save()
    return redirect('home')

@login_required(login_url='signin')
def saves(request):
    
    user_saved_posts = Save.objects.filter(user=request.user).select_related('post')

    saves = [saved_post.post for saved_post in user_saved_posts]
    
    saved_post_ids = [post.id for post in saves]

    posts = (
        Post.objects.filter(id__in=saved_post_ids)
        .annotate(like_count=Count('post_likes'))
    )
    
    liked_posts = Like.objects.filter(user=request.user).values_list('post__id', flat=True)
    saved_posts = Save.objects.filter(user=request.user).values_list('post__id', flat=True)

    return render(request, 'save.html', {
        'posts': posts,
        'liked_posts' : liked_posts,
        'saved_posts' : saved_posts,
    })
