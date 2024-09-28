from django import template

register = template.Library()

@register.filter
def get_community_role(user_communities, community_id):
    for community in user_communities:
        if community.id == community_id:
            return community.role
    return None