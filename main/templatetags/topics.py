from django import template
from main.models import Topic

register = template.Library()

@register.simple_tag
def get_global_topics():
    return Topic.objects.all()