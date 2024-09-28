import uuid 
from django.db import models
from account.models import User

# Create your models here.
class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # topics = ["Anime & Cosplay", "Art", "Business & Finance", "Collectibles & Other Hobbies", "Education & Career", "Fashion & Beauty", "Food & Drinks", "Games","Home & Garden","Humanities & Law", "Internet Culture", "Movies & TV", "Music", "Nature & Outdoors", "News & Politics", "Places & Travel", "Pop Culture", "Q&As & Stories", "Reading & Writing", "Sciences", "Spooky", "Sports", "Technology", "Vehicles", "Wellness", "Mature Topics"]


class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = "private", "Private"
        RESTRICTED = 'restricted', 'Restricted'
    name = models.CharField(max_length=64)
    visibility = models.CharField(max_length=10, choices=Visibility.choices)

    about = models.TextField(max_length = 255)
    avatar = models.TextField(max_length = 1024)
    banner = models.TextField(max_length = 1024)
    members_nickname = models.CharField(max_length=64, default="Members")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Communities"

class CommunityTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('community', 'topic')
        constraints = [
            models.UniqueConstraint(fields=['community', 'topic'], name='unique_community_topic')
        ]

class CommunityRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommunityMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = "moderator", "Moderator"
        MEMBER = 'member', 'Member'
    role = models.CharField(max_length=9, choices=Role.choices, null = False, default = Role.MEMBER)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('community', 'user')
        constraints = [
            models.UniqueConstraint(fields=['community', 'user'], name='unique_community_member')
        ]