from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib.auth.decorators import login_required
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
from interactions.models import Post, Like, Comment
from decouple import config

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')

last_sent_times = {}

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_input = request.POST.get('email')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(email=email_input).exists():
                messages.error(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email_input, password=password, first_name=first_name, last_name=last_name)

                new_profile = Profile.objects.create(user=user, last_name=last_name, first_name=first_name)

                new_profile.save()

                auth.login(request, user)
                return redirect('signin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'registrations/signup.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            request.session['user_email'] = user.email
            return redirect('verification')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'registrations/signin.html')

def send_verification_code( email):
    current_time = time.time()
    if email in last_sent_times and current_time - last_sent_times[email] < 60:
        return None
    
    code = ''.join(str(random.randint(0, 9)) for _ in range(6))  
    sender_email = config('EMAIL')
    password = config('PASSWORD')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Verification Code'

    body = f'Your verification code is: {code}'
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
    
        last_sent_times[email] = current_time
        return code
    
    except Exception as e:
        print(str(e))
        return None

def verification(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')

        if user_email:
            entered_code = ''.join(request.POST.get(f'digit{i+1}') for i in range(6))
            expected_code = request.session.get('verification_code')

            if entered_code == expected_code:
                user = User.objects.get(email=user_email)
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid code. Please try again.')
                return render(request, 'registrations/verification.html', {'email': user_email})
        else:
            messages.error(request, 'User email not found.')
            return redirect('signin')
    else: 
        user_email = request.session.get('user_email')

        if user_email:
            code = send_verification_code(user_email)
            if code:
                request.session['verification_code'] = code
                return render(request, 'registrations/verification.html', {'email': user_email})
            else:
                messages.error(request, 'Please try again later.')
                return redirect('signin')
        else:
            messages.error(request, 'User email not found.')
            return redirect('signin')
        
@login_required(login_url='signin')
def profile_detail(request, profile_id):
    profile = Profile.objects.get(user=profile_id)
    posts = Post.objects.filter(author=profile_id)
    is_following = profile.followers.filter(pk=request.user.profile.pk).exists()

    comments = 0
    likes = 0
    for post in posts:
        likes+=Like.objects.filter(post=post).count()
        comments+=Comment.objects.filter(post=post).count()

    like_count = ''
    comment_count = ''

    if likes > 999:
        like_count+=str(likes//1000)
        like_count+='.'
        like_count+=str(likes//100)[0]
        like_count+='k'
    else:
        like_count = str(likes)

    if comments > 999:
        comment_count+=str(comments//1000)
        comment_count+='.'
        comment_count+=str(comments//100)[0]
        comment_count+='k'
    else:
        comment_count = str(comments)


    return render(request, 'profile.html', {'profile': profile, 'is_following': is_following, 'posts':posts, 'like_count':like_count, 'view_count':comment_count})

@login_required(login_url='signin')
def follow_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.profile != profile:
        request.user.profile.follows.add(profile)
    return redirect('profile_detail', profile_id=profile_id)

@login_required(login_url='signin')
def unfollow_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.profile != profile:
        request.user.profile.follows.remove(profile)
    return redirect('profile_detail', profile_id=profile_id)

@login_required(login_url='signin')
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=request.user)


    comments = 0
    likes = 0
    for post in posts:
        likes+=Like.objects.filter(post=post).count()
        comments+=Comment.objects.filter(post=post).count()
        

    comment_count = ''
    like_count = ''

    if likes > 999:
        like_count+=str(likes//1000)
        like_count+='.'
        like_count+=str(likes//100)[0]
        like_count+='k'
    else:
        like_count = str(likes)

    if comments > 999:
        comment_count+=str(comments//1000)
        comment_count+='.'
        comment_count+=str(comments//100)[0]
        comment_count+='k'
    else:
        comment_count = str(comments)

    return render(request, 'my_profile.html', {'profile':profile, 'posts':posts, 'like_count':like_count, 'comment_count':comment_count})

@login_required(login_url='signin')
def settings(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        profile_img = request.FILES.get('profile_img')  
        bio = request.POST.get('bio')  
        
        if profile_img or bio:
            if profile_img:
                profile.profile_img = profile_img
            profile.bio = bio
            profile.save()
            return redirect('my_profile')

    return render(request, 'settings.html', {'profile' : profile})

@login_required(login_url='signin')
def search(request):
    user = None
    if request.method == 'POST':
        username = request.POST.get('username')
        users = User.objects.filter(username=username)

        if users.exists():
            user = users.first()
            profile = Profile.objects.get(user=user)
            is_following = profile.followers.filter(pk=request.user.profile.pk).exists()
            
            return render(request, 'search.html', {'profile': profile, 'is_following':is_following})
        
        messages.error(request, 'Profile does not exist')
        return render(request, 'search.html', {'user': user})
    else:
        user = User.objects.none()
    return render(request, 'search.html', {'user': user})

@login_required(login_url='signin')
def follow_profile_search(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.profile != profile:
        request.user.profile.follows.add(profile)
    return redirect('search') 

@login_required(login_url='signin')
def unfollow_profile_search(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.profile != profile:
        request.user.profile.follows.remove(profile)
    return redirect('search') 

