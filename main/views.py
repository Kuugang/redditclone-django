import os
from datetime import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from google.oauth2 import id_token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from google.auth.transport import requests as google_requests
from django.db import IntegrityError

from . import models

# Decorators
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .utils import upload_image 

User = get_user_model()

@csrf_exempt
def auth_receiver(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    token = request.POST.get('credential')
    if not token:
        return HttpResponse(status=400)

    try:
        user_data = id_token.verify_oauth2_token(
            token, google_requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
        print("User data:", user_data)
    except ValueError as e:
        print("Token verification error:", str(e))
        return HttpResponse(status=403)

    email = user_data['email']
    first_name = user_data.get('given_name', '')
    last_name = user_data.get('family_name', '')

    user, created = User.objects.get_or_create(email=email, defaults={
        'username': f"{first_name} {last_name}",
        'avatar': user_data.get("picture")
    })

    if created:
        user.set_unusable_password()
        user.save()

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    return HttpResponseRedirect(reverse('dashboard'))

def dashboard(request):
    posts = models.Post.objects.all()
    return render(request, 'dashboard.html', {'posts': posts})

@require_http_methods(["POST"])
def sign_in(request):
    email_or_username = request.POST.get('email_or_username')
    password = request.POST.get('password')
    user = authenticate(request, username=email_or_username, email=email_or_username, password=password)
    if user is not None:
        login(request, user)
        return redirect('dashboard')
    else:
        messages.error(request, 'Invalid email or password')
        return redirect('dashboard')

@require_http_methods(["POST"])
def sign_up(request):
    data = dict(request.POST.items())
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # OPTIONAL FIELDS
    bio = data.get("bio")
    birth_date = data.get("birth_date")
    avatar = request.FILES.get("avatar")

    if User.objects.filter(username=username).exists():
        # messages.error(request, "Username is already taken.")
        return redirect('dashboard')
    if User.objects.filter(email=email).exists():
        # messages.error(request, "Email is already taken.")
        return redirect('dashboard')
    try:

        if birth_date:
            try:
                birth_date = datetime.strptime(birth_date, "%m/%d/%Y").date()
            except ValueError:
                raise ValidationError("Invalid date format. Please use MM/DD/YYYY.")
        user = User.objects.create_user(username, email, password)
        user.bio = bio if bio else None 
        user.birth_date = birth_date if birth_date else None

        if avatar:
            avatar_public_URL = upload_image(avatar, "userAvatar")
            user.avatar = avatar_public_URL

        user.save()
        # messages.success(request, "Account successfully created!")
        return redirect('dashboard')
    except IntegrityError:
        # messages.error(request, "An error occurred while creating your account. Please try again.")
        return redirect('dashboard')
    
@require_http_methods(["GET"])
def check_availability(request):
    username = request.GET.get('username')
    email = request.GET.get('email')

    print(username)
    print(email)

    response_data = {
        'username_available': not User.objects.filter(username=username).exists(),
        'email_available': not User.objects.filter(email=email).exists(),
    }

    return JsonResponse(response_data)

def handle_logout(request):
    logout(request)
    return redirect('dashboard')

@require_http_methods(["POST"])
def create_community(request):
    data = dict(request.POST.items())
    files = dict(request.FILES.items())

    name = data.get('name')
    about = data.get('about')
    visibility = data.get('visibility')
    topics = request.POST.getlist("topics")
    banner = files.get('banner')
    avatar = files.get('avatar')

    avatar_public_URL = upload_image(avatar, "communityAvatar")
    banner_public_URL = upload_image(banner, "communityBanner")
    
    if avatar_public_URL and banner_public_URL:
        community = models.Community(name = name, visibility = visibility, about = about, avatar = avatar_public_URL, banner = banner_public_URL)
        community.save()

        member = models.CommunityMember(community = community, user = request.user, role = 'admin')
        member.save()
        
        for topic in topics:
            communityTopic = models.CommunityTopic(topic = models.Topic.objects.get(id=topic), community = community)
            communityTopic.save()

        return redirect('dashboard')
    return redirect('dashboard')

def community(request, community_name):
    community = get_object_or_404(models.Community, name=community_name)
    return render(request, 'community.html', {'community': community})

def submit(request):
    return render(request, 'submit.html')

def create_post(request):
    data = dict(request.POST.items())
    title = data.get("title")
    content = data.get("content")
    community = data.get("community")
    community = models.Community.objects.get(id=community)
    # TODO
    # flairs = data.get("flairs")

    post = models.Post(title = title, content = content, community = community, user = request.user)
    post.save()

    return redirect('submit')

def upload_post_image(request):
    image = request.FILES.get("file")
    print(image)

    url = upload_image(image, "postImage")

    print(url)

    response_data = {
        'url' : url
    }

    return JsonResponse(response_data)

def edit_community_appearance(request):
    avatar = request.FILES.get("avatar")
    banner = request.FILES.get("banner") 
    community_id = request.POST.get("community_id")
    community = models.Community.objects.get(id=community_id)

    banner_url = upload_image(banner, "communityBanner") if banner else None 
    avatar_url = upload_image(avatar, "communityAvatar") if avatar else None

    if banner_url:
        community.banner = banner_url
    if avatar_url:
        community.avatar = avatar_url

    community.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
