from django.contrib.auth import get_user_model
# from .models import UserProfile

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
