import os
import requests

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from django.shortcuts import render, redirect
from django.contrib import messages
from google.auth.transport import requests as google_requests

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