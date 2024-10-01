# Generated by Django 5.1.1 on 2024-10-01 14:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_rename_title_communityevent_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='communityevent',
            name='check_event_dates',
        ),
        migrations.RemoveConstraint(
            model_name='communityevent',
            name='check_event_times',
        ),
        migrations.RenameField(
            model_name='communityevent',
            old_name='event_end_date',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='communityevent',
            old_name='event_end_time',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='communityevent',
            old_name='event_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='communityevent',
            old_name='event_start_date',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='communityevent',
            old_name='event_start_time',
            new_name='start_time',
        ),
        migrations.AddConstraint(
            model_name='communityevent',
            constraint=models.CheckConstraint(condition=models.Q(('start_date__lte', models.F('end_date'))), name='check_event_dates'),
        ),
        migrations.AddConstraint(
            model_name='communityevent',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('start_date', models.F('end_date')), ('start_time__lt', models.F('end_time'))), ('start_date__lt', models.F('end_date')), _connector='OR'), name='check_event_times'),
        ),
    ]