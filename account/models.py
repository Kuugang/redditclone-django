from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    birth_date = models.DateField(null = True)
    avatar = models.TextField(max_length = 1024, null = True)
    bio = models.TextField(max_length = 128, null = True)

    updated_at = models.DateTimeField(null = True, auto_now=True)