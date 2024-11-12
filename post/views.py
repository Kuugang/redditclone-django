import os, uuid
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from django.core.serializers import serialize
from . import models

from community.models import Community, CommunityTopic, CommunityRule, CommunityEvent, CommunityPostReport

from django.core.exceptions import ValidationError

# Utils
from common.utils import upload_image, upload_local_image
from django.utils.dateformat import format

 

def post(request, post_id):
    post_instance = get_object_or_404(models.Post, id=post_id)
    root_comments = models.Comment.objects.filter(post=post_instance, parent=None)
    child_comments = models.Comment.objects.filter(post=post_instance).exclude(parent=None)
    
    # If you want to do something with root_comments or log something, do it here

    return render(request, 'components/post/post_detail.html', {
        'post': post_instance,
        'root_comments': root_comments,
        'child_comments': child_comments
    })


def submit(request, community_name=None):
    context = {}

    if community_name:
        community = get_object_or_404(Community, name=community_name)
        community_rules = CommunityRule.objects.filter(community=community)
        community_topics = CommunityTopic.objects.filter(community=community)
        community_events = CommunityEvent.objects.filter(community=community)
        context['community'] = community
        context['community_rules'] = community_rules
        context['community_topics'] = community_topics
        context['community_events'] = community_events
        context['submit'] = True

    return render(request, 'components/post/submit.html', context)

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

    return redirect('community:community', community_name=community.name)

def upload_post_image(request):
    image = request.FILES.get("file")
    if os.getenv("ENV") == "development":
        url = upload_local_image(image, "postImage")
    else:
        url = upload_image(image, "postImage")


    response_data = {
        'url' : url
    }

    return JsonResponse(response_data)

#deo code

def comment(request, post_id):
    post_instance = get_object_or_404(models.Post, id=post_id)
    content = request.POST.get("comment")
    
    if not content:
        return JsonResponse({"error": "Comment content is required"}, status=400)

    comment = models.Comment.objects.create(
        user=request.user,
        post=post_instance,
        content=content
    )

    comment_object = models.Comment.objects.filter(id=comment.id).values('created_at')[0]
    formatted_date = format(comment_object['created_at'], 'M. j, Y, P')

    comment_data = serialize('json', [comment])
    comment_json = json.loads(comment_data)[0]['fields']
    comment_json["id"] = json.loads(comment_data)[0]['pk']
    comment_json["created_at"] = formatted_date


    return JsonResponse(comment_json)

def delete_comment(request):
    comment_id = request.POST.get("comment_id")
    comment = get_object_or_404(models.Comment, id=uuid.UUID(str(comment_id)), user = request.user)
    comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def reply_to_comment(request, comment_id):
    if not request.headers.get('X-CSRFToken'):
        return JsonResponse({'error': 'CSRF token missing'}, status=403)

    data = json.loads(request.body)
    content = data.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'Content is required'}, status=400)

    parent_comment = models.Comment.objects.select_related('post', 'user').get(id=comment_id)

    reply = models.Comment.objects.create(
        content=content,
        post=parent_comment.post,
        parent=parent_comment,
        user=request.user
    )

    formatted_date = format(reply.created_at, 'M. j, Y, P')

    avatar = None
    if hasattr(reply.user, 'avatar'):
        
        if isinstance(reply.user.avatar, str):
            avatar = reply.user.avatar  
        elif hasattr(reply.user.avatar, 'url'):
            avatar = reply.user.avatar.url  
    reply_json = {
        'id': str(reply.id),
        'content': reply.content,
        'created_at': formatted_date,
        'user': {
            'username': reply.user.username,
            'avatar': avatar,
        },
        'parent_id': str(parent_comment.id)
    }

    return JsonResponse(reply_json)


   
def vote(request, post_id, vote_type):
    vote = models.Vote.objects.filter(user=request.user, post=models.Post.objects.get(id=post_id))

    if vote:
        if vote[0].vote == vote_type:
            vote[0].delete()
        else:
            vote[0].vote = vote_type
            vote = vote[0]
            vote.save()
    else:
        vote = models.Vote(user=request.user, post=models.Post.objects.get(id=post_id), vote=vote_type)
        vote.save()

    return JsonResponse(
        {'status': True}
    )

def delete_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(models.Post, id=uuid.UUID(str(post_id)), user=request.user)
    post.delete()

    referer_url = request.META.get('HTTP_REFERER', '')

    if "community" in referer_url:
        community_name = post.community.name 
        return redirect('community:community', community_name=community_name)
    else:
        return redirect('dashboard')

def save_post(request):
    post_id = request.POST.get('post_id')
    post = models.Post.objects.get(id=uuid.UUID(str(post_id)))
    user = request.user

    user_saved_post = models.UserSavedPost(user=user, post=post)
    user_saved_post.save()

    return JsonResponse({'success': True})

def unsave_post(request):
    post_id = request.POST.get('post_id')
    post = models.Post.objects.get(id=uuid.UUID(str(post_id)))
    user = request.user

    user_saved_post = models.UserSavedPost.objects.filter(user=user, post=post)
    user_saved_post.delete()

    return JsonResponse({'success': True})

def edit_post(request, post_id):
    if request.method == "GET":
        post = models.Post.objects.get(id=uuid.UUID(str(post_id)))
        community = Community.objects.get(id=post.community_id)
        return render(request, 'components/post/edit_post.html', {'post': post, 'community': community})
    if request.method == "POST":
        data = dict(request.POST.items())
        post_id = data.get("post_id")
        post = models.Post.objects.get(id=uuid.UUID(str(post_id)))
        content = data.get("post_content")
        post.content = content
        post.save()

        return redirect('post:post', post_id=post.id)

def report_post(request):
    data = dict(request.POST.items())
    post_id = data.get("post_id")

    post = models.Post.objects.get(id=uuid.UUID(str(post_id)))
    category = data.get("category")
    description = data.get("description")

    report = CommunityPostReport(reporter=request.user, post=post, category = category, description = description)
    report.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))