import os, uuid, requests

from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

# Decorators
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# GOOGLE AUTH
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Utils
from common.utils import upload_image, upload_local_image

# Models
from post.models import Post

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

    return HttpResponseRedirect('/')

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
    avatar = request.FILES.get("avatar")

    if User.objects.filter(username=username).exists():
        return redirect('dashboard')
    if User.objects.filter(email=email).exists():
        return redirect('dashboard')
    try:
        user = User.objects.create_user(username, email, password)
        user.bio = bio if bio else None 

        if avatar:
            avatar_public_URL = ""
            if os.getenv("ENV") == "development":
                avatar_public_URL = upload_local_image(avatar, "userAvatar")
            else:
                avatar_public_URL = upload_image(avatar, "userAvatar")
            user.avatar = avatar_public_URL

        user.save()
        return redirect('dashboard')
    except IntegrityError:
        return redirect('dashboard')



@require_http_methods(["GET"])
def check_availability(request):
    username = request.GET.get('username')
    email = request.GET.get('email')

    response_data = {
        'username_available': not User.objects.filter(username=username).exists(),
        'email_available': not User.objects.filter(email=email).exists(),
    }

    return JsonResponse(response_data)

def dashboard(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'dashboard.html', {'posts': posts})