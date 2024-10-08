# Generated by Django 5.1.1 on 2024-09-22 04:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_community_options_alter_post_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communityrule',
            name='rule',
        ),
        migrations.AddField(
            model_name='communityrule',
            name='description',
            field=models.CharField(default=django.utils.timezone.now, max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='communityrule',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=64),
            preserve_default=False,
        ),
    ]
