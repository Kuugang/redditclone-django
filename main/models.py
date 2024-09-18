import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    birth_date = models.DateField(null = True)
    avatar = models.TextField(max_length = 1024, null = True)
    bio = models.TextField(max_length = 128, null = True)

    updated_at = models.DateTimeField(null = True, auto_now=True)

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # topics = ["Anime & Cosplay", "Art", "Business & Finance", "Collectibles & Other Hobbies", "Education & Career", "Fashion & Beauty", "Food & Drinks", "Games","Home & Garden","Humanities & Law", "Internet Culture", "Movies & TV", "Music", "Nature & Outdoors", "News & Politics", "Places & Travel", "Pop Culture", "Q&As & Stories", "Reading & Writing", "Sciences", "Spooky", "Sports", "Technology", "Vehicles", "Wellness", "Mature Topics"]

    # TODO init for this/ automatically add topics


class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = "private", "Private"
        RESTRICTED = 'restricted', 'Restricted'
    name = models.CharField(max_length=255)
    visibility = models.CharField(max_length=10, choices=Visibility.choices)

    about = models.TextField(max_length = 64)
    avatar = models.TextField(max_length = 1024)
    banner = models.TextField(max_length = 1024)

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
    rule = models.CharField(max_length=2048)

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


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.TextField(max_length = 64)
    content = models.TextField(max_length = 2048)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Vote(models.Model):
    class VoteType(models.TextChoices):
        UPVOTE = 'upvote', 'Upvote'
        DOWNVOTE = 'downvote', 'Downvote'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.CharField(max_length=8, choices=VoteType.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_vote')
        ]

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_deleted = models.BooleanField(default=False)
    content = models.TextField(max_length=2048)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
