# Generated by Django 5.1.1 on 2024-09-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_communityrule_rule_communityrule_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='members_nickname',
            field=models.CharField(default='Members', max_length=64),
        ),
    ]