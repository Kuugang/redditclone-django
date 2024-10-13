from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    display_name = models.CharField(max_length = 64, null = True)
    birth_date = models.DateField(null = True)
    avatar = models.TextField(max_length = 2048, null = True)
    banner = models.TextField(max_length = 2048, null = True)
    about = models.TextField(max_length = 128, null = True)

    updated_at = models.DateTimeField(null = True, auto_now=True)

class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower')