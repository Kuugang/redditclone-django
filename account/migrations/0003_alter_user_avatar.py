# Generated by Django 5.1.1 on 2024-10-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
