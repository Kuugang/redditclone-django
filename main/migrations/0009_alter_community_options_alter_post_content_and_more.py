# Generated by Django 5.1.1 on 2024-09-21 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_communitymember_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'verbose_name_plural': 'Communities'},
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=40000),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=300),
        ),
    ]
