import uuid, os
from datetime import datetime
from . import models
from post.models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from common.utils import upload_image, upload_local_image

def community(request, community_name):
    community = get_object_or_404(models.Community, name=community_name)
    community_rules = models.CommunityRule.objects.filter(community=community)
    community_topics = models.CommunityTopic.objects.filter(community=community)
    community_events = models.CommunityEvent.objects.filter(community=community)

    posts = Post.objects.filter(community=community).order_by('-created_at')

    context = {
        'community': community, 
        'community_rules': community_rules, 
        'community_topics': community_topics,
        'topics' : {topic.topic for topic in community_topics},
        'posts': posts,
        'community_events': community_events
    }

    return render(request, 'community.html', context)

@require_http_methods(["POST"])
def create_community(request):
    data = dict(request.POST.items())
    files = dict(request.FILES.items())

    community_name = data.get('community_name')
    about = data.get('about')
    visibility = data.get('visibility')
    topics = request.POST.getlist("topics")
    banner = files.get('banner')
    avatar = files.get('avatar')
    avatar_public_URL = ""
    banner_public_URL = ""

    if os.getenv("ENV") == "development":
        avatar_public_URL = upload_local_image(avatar, "communityAvatar")
        banner_public_URL = upload_local_image(banner, "communityBanner")
    else:
        avatar_public_URL = upload_image(avatar, "communityAvatar")
        banner_public_URL = upload_image(banner, "communityBanner")
    
    if avatar_public_URL and banner_public_URL:
        community = models.Community(name = community_name, visibility = visibility, about = about, avatar = avatar_public_URL, banner = banner_public_URL)
        community.save()

        member = models.CommunityMember(community = community, user = request.user, role = 'admin')
        member.save()
        
        for topic in topics:
            communityTopic = models.CommunityTopic(topic = models.Topic.objects.get(id=topic), community = community)
            communityTopic.save()

        return redirect('dashboard')
    return redirect('dashboard')

def join_community(request, community_name):
    community = models.Community.objects.get(name=community_name)
    member = models.CommunityMember(community = community, user = request.user, role = 'member')
    member.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def edit_community_appearance(request):
    avatar = request.FILES.get("avatar")
    banner = request.FILES.get("banner") 
    community_id = request.POST.get("community_id")
    community = models.Community.objects.get(id=community_id)

    avatar_url = ""
    banner_url = ""

    if os.getenv("ENV") == "development":
        avatar_url = upload_local_image(avatar, "communityAvatar")
        banner_url = upload_local_image(banner, "communityBanner")
    else:
        avatar_url = upload_image(avatar, "communityAvatar")
        banner_url = upload_image(banner, "communityBanner")

    if banner_url:
        community.banner = banner_url
    if avatar_url:
        community.avatar = avatar_url

    community.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


def create_community_rule(request):
    data = dict(request.POST.items())

    rule_name = data.get("rule_name")
    rule_description = data.get("rule_description")
    community_id = data.get("community_id")
    community = models.Community.objects.get(id=community_id)

    rule = models.CommunityRule(community = community, name = rule_name, description = rule_description)
    rule.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    
def edit_community_rule(request):
    data = dict(request.POST.items())

    rule_name = data.get("rule_name")
    rule_description = data.get("rule_description")
    rule_id = data.get("rule_id")
    community_rule = get_object_or_404(models.CommunityRule, id=rule_id)

    if(rule_name):
        community_rule.name = rule_name
    if(rule_description):
        community_rule.description = rule_description
    community_rule.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def edit_community_details(request):
    data = dict(request.POST.items())
    community_id = data.get("community_id")
    community = models.Community.objects.get(id=community_id)
    about = data.get("community_about")
    members_nickname = data.get("community_members_nickname")

    community.about = about
    community.members_nickname = members_nickname
    community.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


def delete_community_rule(request):
    rule_id = request.POST.get("rule_id")
    models.CommunityRule.objects.filter(id=rule_id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


def edit_community_topics(request):
    data = dict(request.POST.items())
    topics = request.POST.getlist("topics")
    community_id = data.get("community_id")
    
    existing_topics = set(models.CommunityTopic.objects.filter(community_id=community_id).values_list('topic_id', flat=True))
    new_topics = set(uuid.UUID(topic_id) for topic_id in topics)
    
    topics_to_add = new_topics - existing_topics
    topics_to_remove = existing_topics - new_topics
    
    for topic_id in topics_to_remove:
        models.CommunityTopic.objects.filter(community_id=community_id, topic_id=topic_id).delete()
    
    for topic_id in topics_to_add:
        topic = models.Topic.objects.get(id=topic_id)
        community_topic = models.CommunityTopic(topic=topic, community_id=community_id)
        community_topic.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@require_http_methods(["GET"])
def check_community_name_availability(request):
    name = request.GET.get('community_name')
    response_data = {
        'name_available': not models.Community.objects.filter(name=name).exists(),
    }
    return JsonResponse(response_data)

def create_event(request, community_name):
    if request.method == "POST":
        data = dict(request.POST.items())
        community = models.Community.objects.get(id=uuid.UUID(data.get('community_id')))
        name = data.get("name")
        host = request.user
        description = data.get('description')

        event_image = request.FILES.get('event_image')
        location = data.get('location')

        event_start_date = datetime.strptime(data.get('event_start_date'), '%m/%d/%Y').strftime('%Y-%m-%d')
        event_end_date = datetime.strptime(data.get('event_end_date'), '%m/%d/%Y').strftime('%Y-%m-%d')

        event_start_time = data.get('event_start_time')
        event_end_time = data.get('event_end_time')

        event_image_url = ""
        if os.getenv("ENV") == "development":
            event_image_url = upload_local_image(event_image, "eventImage")
        else:
            event_image_url = upload_image(event_image, "eventImage")
        event = models.CommunityEvent(community=community, host=host, name = name, description=description, image=event_image_url, location=location, start_date=event_start_date, end_date=event_end_date, start_time=event_start_time, end_time=event_end_time) 
        event.save()

        return redirect('community:community', community_name=community.name)
    else:
        context = {}
        if community_name:
            community = get_object_or_404(models.Community, name=community_name)
            community_rules = models.CommunityRule.objects.filter(community=community)
            community_topics = models.CommunityTopic.objects.filter(community=community)
            context['community'] = community
            context['community_rules'] = community_rules
            context['community_topics'] = community_topics
            context['submit'] = True

        return render(request, 'components/community/create_event.html', context)

def community_event_detail(request, community_name, event_id):
    event = models.CommunityEvent.objects.get(id=event_id)
    community_events = models.CommunityEvent.objects.filter(community=event.community)
    return render(request, "components/community/community_event_detail.html", {"event": event, "community_events": community_events})