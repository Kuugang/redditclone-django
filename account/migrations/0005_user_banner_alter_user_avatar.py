# Generated by Django 5.1.1 on 2024-10-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_bio_user_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner',
            field=models.TextField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(max_length=2048, null=True),
        ),
    ]