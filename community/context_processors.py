from django.contrib.auth import get_user_model
from . import models

def user_communities_context(request):
    query = """
        SELECT c.*, cm.role
        FROM community_community c
        LEFT JOIN community_communitymember cm ON cm.community_id = c.id
        WHERE cm.user_id = %s
        ORDER BY c.name;
    """
        
    user_communities = models.Community.objects.raw(query, [request.user.id])

    return {
        'user_communities': user_communities
    }