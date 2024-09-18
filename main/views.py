import os
import requests

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from google.oauth2 import id_token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from google.auth.transport import requests as google_requests

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
    return render(request, 'dashboard.html')

def sign_in(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')
        user = authenticate(request, username=email_or_username, email=email_or_username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('dashboard')
    return redirect('dashbord')

def register(request):
    return render(request, 'dashboard.html')

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