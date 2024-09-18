from django.core.management.base import BaseCommand
from main.models import Topic
import uuid

class Command(BaseCommand):
    help = 'Populates the Topic model with predefined topics'

    TOPICS = [
        "Anime & Cosplay", "Art", "Business & Finance", "Collectibles & Other Hobbies",
        "Education & Career", "Fashion & Beauty", "Food & Drinks", "Games", "Home & Garden",
        "Humanities & Law", "Internet Culture", "Movies & TV", "Music", "Nature & Outdoors",
        "News & Politics", "Places & Travel", "Pop Culture", "Q&As & Stories", "Reading & Writing",
        "Sciences", "Spooky", "Sports", "Technology", "Vehicles", "Wellness", "Mature Topics"
    ]

    def handle(self, *args, **kwargs):
        for name in self.TOPICS:
            topic, created = Topic.objects.get_or_create(
                name=name,
                defaults={'id': uuid.uuid4()}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Topic "{name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Topic "{name}" already exists'))

