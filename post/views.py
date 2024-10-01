import os

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.shortcuts import render, redirect

from . import models
from community.models import Community, CommunityTopic, CommunityRule

# Utils
from common.utils import upload_image, upload_local_image

def post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    return render(request, 'components/post/post_detail.html', {'post': post})

def submit(request, community_name=None):
    context = {}

    if community_name:
        community = get_object_or_404(Community, name=community_name)
        community_rules = CommunityRule.objects.filter(community=community)
        community_topics = CommunityTopic.objects.filter(community=community)
        context['community'] = community
        context['community_rules'] = community_rules
        context['community_topics'] = community_topics
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

def comment(request):
    return "wiggy"


def reply_to_comment(request):
    return "oscarrrrr"

def vote(request, post_id, vote_type):

    vote = models.Vote.objects.filter(user=request.user, post=models.Post.objects.get(id=post_id))
    print(vote)
    if vote:
        vote[0].vote = vote_type
        vote = vote[0]
    else:
        vote = models.Vote(user=request.user, post=models.Post.objects.get(id=post_id), vote=vote_type)
    vote.save()
   # return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    response_data = {
        'vote' : vote
    }
    return JsonResponse(response_data)

def downvote(request):
    return -1

#deo code