# Generated by Django 5.1.1 on 2024-11-28 18:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_rename_community_communityinvite_community'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='communityeventparticipant',
            unique_together={('event', 'participant')},
        ),
        migrations.AddConstraint(
            model_name='communityeventparticipant',
            constraint=models.UniqueConstraint(fields=('event', 'participant'), name='unique_event_participant'),
        ),
    ]