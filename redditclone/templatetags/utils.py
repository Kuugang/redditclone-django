import os

from django import template

from post.models import Comment, PostVote, CommentVote

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

@register.filter
def get_post_vote_counts(post):
    upvotes = PostVote.objects.filter(post=post, vote="upvote").count()
    downvotes = PostVote.objects.filter(post=post, vote="downvote").count()
    return upvotes - downvotes

@register.filter
def get_comment_vote_counts(comment):
    upvotes = CommentVote.objects.filter(comment=comment, vote="upvote").count()
    downvotes = CommentVote.objects.filter(comment=comment, vote="downvote").count()
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

@register.filter
def has_non_deleted_children(comments):
    """
    Recursively checks if any comment or its children are not deleted.
    :param comments: List of dictionaries, each containing a comment and its children.
    :return: True if there is at least one non-deleted comment in the tree, False otherwise.
    """
    def recursive_check(comments_list):
        for comment in comments_list:
            if not comment['comment'].is_deleted:
                return True
            if comment['children']:
                if recursive_check(comment['children']):
                    return True
        return False

    return recursive_check(comments)