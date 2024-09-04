from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if email:
                user = UserModel.objects.get(email=email)
            else:
                user = UserModel.objects.get(username=username)
                
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None