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

class CommunityEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    image = models.CharField(max_length=1024)
    location = models.CharField(max_length=255)

    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lte=models.F('end_date')),
                name='check_event_dates'
            ),
            models.CheckConstraint(
                check=(
                    models.Q(start_date=models.F('end_date')) &
                    models.Q(start_time__lt=models.F('end_time'))
                ) | models.Q(start_date__lt=models.F('end_date')),
                name='check_event_times'
            )
        ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommunityEventParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)