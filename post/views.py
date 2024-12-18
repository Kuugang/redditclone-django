import os, uuid
from uuid import UUID
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from django.core.serializers import serialize
from . import models

from community.models import Community, CommunityTopic, CommunityRule, CommunityEvent, CommunityPostReport

from django.core.exceptions import ValidationError

# Utils
from common.utils import upload_image, upload_local_image, get_child_comments
from django.utils.dateformat import format

import logging

logger = logging.getLogger(__name__)

def post(request, post_id):
    try:
        UUID(str(post_id), version=4)
    except ValueError:
        raise Http404("Invalid post ID format")

    post_instance = get_object_or_404(models.Post, id=post_id)
    root_comments = models.Comment.objects.filter(post=post_instance, parent=None)
    comments = []
    for comment in root_comments:
        comment_data = {
            'comment': comment,
            'depth': 0,
            'children': get_child_comments(comment, 1)
        }
        comments.append(comment_data)
    comments.reverse()
    return render(request, 'components/post/post_detail.html', {
        'post': post_instance,
        'root_comments': root_comments,
        'comments': comments
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

def create_post(request, community_name):
    data = dict(request.POST.items())
    title = data.get("title")
    content = data.get("content")
    community = models.Community.objects.get(name=community_name)
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


def comment(request, post_id):
    post_instance = get_object_or_404(models.Post, id=post_id)
    content = request.POST.get("comment")
    parent_id = request.POST.get("parent_id")


    if(parent_id):
        parent  = get_object_or_404(models.Comment, id=uuid.UUID(str(parent_id)))

        comment = models.Comment.objects.create(
            user=request.user,
            post=post_instance,
            content=content,
            parent = parent
        )
    else:
        comment = models.Comment.objects.create(
            user=request.user,
            post=post_instance,
            content=content,
        )
    comment.save()
    
    if not content:
        return JsonResponse({"error": "Comment content is required"}, status=400)


    comment_object = models.Comment.objects.filter(id=comment.id).values('created_at')[0]
    formatted_date = format(comment_object['created_at'], 'M. j, Y, P')

    comment_data = serialize('json', [comment])
    comment_json = json.loads(comment_data)[0]['fields']
    comment_json["id"] = json.loads(comment_data)[0]['pk']
    comment_json["created_at"] = formatted_date

    return JsonResponse(comment_json)

def edit_comment(request, comment_id):
    comment = get_object_or_404(models.Comment, id=uuid.UUID(str(comment_id)))
    content = request.POST.get("comment")
    comment.content = content
    comment.save()

    return JsonResponse({'success': True})

def delete_comment(request):
    comment_id = request.POST.get("comment_id")
    comment = get_object_or_404(models.Comment, id=uuid.UUID(str(comment_id)), user = request.user)
    comment.is_deleted = True
    comment.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def vote(request, content_id, vote, type):
    if type == "post":
        vote_object = models.PostVote.objects.filter(user=request.user, post=models.Post.objects.get(id=content_id))
    else:
        vote_object = models.CommentVote.objects.filter(user=request.user, comment=models.Comment.objects.get(id=content_id))

    if vote_object:
        if vote_object[0].vote == vote:
            vote_object[0].delete()
        else:
            vote_object[0].vote = vote 
            vote_object[0].save()
    else:
        if type == "post":
            vote_object = models.PostVote(user=request.user, post=models.Post.objects.get(id=content_id), vote=vote)
        else:
            vote_object = models.CommentVote(user=request.user, comment=models.Comment.objects.get(id=content_id), vote=vote)
        vote_object.save()

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