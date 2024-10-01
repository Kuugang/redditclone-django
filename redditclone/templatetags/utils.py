import os
from django import template
from django.templatetags.static import static
from django.db.models import Count


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
    upvotes = post.vote_set.filter(vote="upvote").count()
    downvotes = post.vote_set.filter(vote="downvote").count()
    return upvotes - downvotes