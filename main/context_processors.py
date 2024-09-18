from django.contrib.auth import get_user_model
# from .models import UserProfile
from . import models

# def user_profile_context(request):
#     user_profile = None
#     if request.user.is_authenticated:
#         try:
#             user_profile = UserProfile.objects.get(user=request.user)
#         except UserProfile.DoesNotExist:
#             pass  # Handle case where profile does not exist
#     return {
#         'user_profile': user_profile
#     }


def user_communities_context(request):
    query = """
        SELECT c.*, cm.role
        FROM main_community c
        LEFT JOIN main_communitymember cm ON cm.community_id = c.id
        WHERE cm.user_id = %s
        ORDER BY c.name;
    """
        
    user_communities = models.Community.objects.raw(query, [request.user.id])

    return {
        'user_communities': user_communities
    }