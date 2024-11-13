import os

from django import template

from post.models import Comment, PostVote

register = template.Library()

@register.simple_tag
def get_image_url(path):
    if not path.startswith('https'):
        path = f"{{% static '{path}' %}}"
        return path
    else:
        return path

@register.filter
def startswith(value, arg):
    return value.startswith(arg)

# @register.filter
# def get_vote_counts(value, arg):
#     counts = len(value) - len(arg)
#     return counts
# wiggy nis jake bisag walay downvote na attribute sa post anion o

@register.filter
def get_vote_counts(post):
    upvotes = PostVote.objects.filter(post=post, vote="upvote").count()
    downvotes = PostVote.objects.filter(post=post, vote="downvote").count()
    return upvotes - downvotes

@register.filter
def get_comment_counts(post):
    count = Comment.objects.filter(post=post).count()
    return count

@register.filter
def get_community_events(community):
    return community.communityevent_set.all()

@register.filter
def get_community_rules(community):
    return community.communityrule_set.all()

@register.filter
def get_community_topics(community):
    return community.communitytopic_set.all()

@register.filter
def get_topics(community):
    return community.communitytopic_set.select_related('topic').values_list('topic__name', flat=True)

@register.filter
def get_community_role(user_communities, community_id):
    for community in user_communities:
        if community.id == community_id:
            return community.role
    return None
