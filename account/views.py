import os, uuid, requests

from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.serializers import serialize
import json

# Decorators
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# GOOGLE AUTH
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Utils
from common.utils import upload_image, upload_local_image

# Models
from post.models import Post, Comment, Vote
from community.models import Community, CommunityMember
from . import models


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
        'username': f"{first_name}{last_name}",
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
    user = request.user  # Get the logged-in user

    # Get private communities where the user is a member
    if(user.is_authenticated):
        private_communities = CommunityMember.objects.filter(
            user=user,
            community__visibility=Community.Visibility.PRIVATE
        ).values_list('community', flat=True)

        posts = Post.objects.filter(
            community__visibility__in=[Community.Visibility.PUBLIC, Community.Visibility.RESTRICTED]
        ) | Post.objects.filter(community__id__in=private_communities)
    else:
        posts = Post.objects.filter(community__visibility=Community.Visibility.PUBLIC or Community.Visibility.RESTRICTED)

    # Order posts by creation date
    posts = posts.order_by('-created_at')

    return render(request, 'dashboard.html', {'posts': posts})

def profile(request):
    return render(request, 'components/account/profile.html')

def profile_settings(request):
    return render(request, 'components/account/profile_settings.html')

def edit_display_name(request):
    display_name = request.POST.get('display_name')
    request.user.display_name = display_name.strip()
    request.user.save()
    return redirect('account:profile_settings')

def edit_about(request):
    about = request.POST.get('about')
    request.user.about = about.strip()
    request.user.save()
    return redirect('account:profile_settings')

def edit_avatar(request):
    avatar = request.FILES.get('avatar')
    if os.getenv("ENV") == "development":
        avatar_public_URL = upload_local_image(avatar, "userAvatar")
    else:
        avatar_public_URL = upload_image(avatar, "userAvatar")
    request.user.avatar = avatar_public_URL
    request.user.save()
    return redirect('account:profile_settings')

def edit_banner(request):
    banner = request.FILES.get('banner')
    if os.getenv("ENV") == "development":
        banner_public_URL = upload_local_image(banner, "userBanner")
    else:
        banner_public_URL = upload_image(banner, "userBanner")
    request.user.banner = banner_public_URL
    request.user.save()
    return redirect('account:profile_settings')

def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    query = """
        SELECT c.*, cm.role
        FROM community_community c
        LEFT JOIN community_communitymember cm ON cm.community_id = c.id
        WHERE cm.user_id = %s
        ORDER BY c.name;
    """
    user_communities = Community.objects.raw(query, [user.id])
    if not request.user.is_anonymous:
        private_communities_user_not_in = set(
            Community.objects.filter(visibility='private')
            .exclude(communitymember__user=request.user)
            .values_list('id', flat=True)
        )
    else:
        private_communities_user_not_in = set(
            Community.objects.filter(visibility='private').values_list('id', flat=True)
        )

    user_posts = Post.objects.filter(user=user).order_by('-created_at')

    if request.user != user:
        user_posts = [post for post in user_posts if post.community_id not in private_communities_user_not_in]


    user_comments = Comment.objects.filter(user=user.id, is_deleted = False).order_by('-created_at')
    if request.user != user:
        user_comments = [comment for comment in user_comments if comment.post.community_id not in private_communities_user_not_in]

    user_overview = sorted(
        list(user_posts) + list(user_comments),
        key=lambda x: x.created_at,
        reverse=True
    )

    userprofile_followers = models.Follower.objects.filter(user=user.id).values_list('follower', flat=True)

    context = {
        'user_profile' : user,
        'user_posts' : user_posts,
        'user_overview' : user_overview,
        'user_comments' : user_comments,
        'user_followers': userprofile_followers,
    }
    return render(request, 'components/account/profile.html', context)

def follow(request, user):
    user = User.objects.get(username=user)
    if not models.Follower.objects.filter(user=user, follower=request.user).exists():
        models.Follower.objects.create(user=user, follower=request.user)
    return redirect('account:user_profile', username=user.username)

def unfollow(request, user):
    user = User.objects.get(username=user)
    models.Follower.objects.filter(user=user, follower=request.user).delete()
    return redirect('account:user_profile', username=user.username)

@csrf_exempt
@require_http_methods(["POST"])
def search(request):
    try:
        data = json.loads(request.body)
        query = data.get('search', '')
        
        # Communities
        public_communities = Community.objects.filter(
            Q(name__icontains=query) & 
            Q(visibility=Community.Visibility.PUBLIC)
        )
        
        restricted_communities = Community.objects.filter(
            Q(name__icontains=query) & 
            Q(visibility=Community.Visibility.RESTRICTED)
        )
        
        # Communities filter for logged-in users
        if request.user.is_authenticated:
            private_communities = Community.objects.filter(
                Q(name__icontains=query) & 
                Q(visibility=Community.Visibility.PRIVATE) &
                Q(communitymember__user=request.user)
            )
            communities = public_communities | restricted_communities | private_communities
        else:
            communities = public_communities | restricted_communities
        
        # Users
        users = User.objects.filter(Q(username__icontains=query) | Q(display_name__icontains=query))
        
        # Posts
        public_posts = Post.objects.filter(
            Q(title__icontains=query) & 
            Q(community__visibility=Community.Visibility.PUBLIC)
        )
        
        restricted_posts = Post.objects.filter(
            Q(title__icontains=query) & 
            Q(community__visibility=Community.Visibility.RESTRICTED)
        )
        
        # Posts filter for logged-in users
        if request.user.is_authenticated:
            private_posts = Post.objects.filter(
                Q(title__icontains=query) & 
                Q(community__visibility=Community.Visibility.PRIVATE) &
                Q(community__communitymember__user=request.user)
            )
            posts = public_posts | restricted_posts | private_posts
        else:
            posts = public_posts | restricted_posts
        
        # Serialize data
        user_data = serialize('json', users)
        community_data = serialize('json', communities)
        post_data = serialize('json', posts)
        
        # Parse JSON
        user_data = json.loads(user_data)
        community_data = json.loads(community_data)
        post_data = json.loads(post_data)

        response_data = {
            'users': [
            {
                'username': user['fields']['username'],
                'display_name': user['fields']['display_name'],
                'avatar': user['fields']['avatar'],
                'banner': user['fields']['banner'],
                'about': user['fields']['about']
            }
            for user in user_data
            ],
            'communities': [
            {
                'name': community['fields']['name'],
                'avatar': community['fields']['avatar'],
                'about': community['fields']['about'],
                'visibility': community['fields']['visibility']
            }
            for community in community_data
            ],
            'posts': [
            {
                'id' : post['pk'],
                'title': post['fields']['title'],
                'content': post['fields']['content'],
                'created_at': post['fields']['created_at']
            }
            for post in post_data
            ]
        }

        return JsonResponse(response_data, safe=False)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def raise_500(request):
    raise Exception("This is a test 500 error.")