# Generated by Django 4.2.12 on 2024-09-04 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
