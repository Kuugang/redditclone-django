from django.contrib import admin
from . import models

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

@admin.register(models.Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'visibility', 'about', 'avatar', 'banner', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

@admin.register(models.CommunityTopic)
class CommunityTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'community', 'topic', 'created_at', 'updated_at')
    search_fields = ('community', 'topic')
    list_filter = ('created_at', 'updated_at')



@admin.register(models.CommunityRule)
class CommunityRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'community', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('community', 'name', 'description')
    list_filter = ('created_at', 'updated_at')


@admin.register(models.CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'community', 'user', 'role', 'created_at', 'updated_at')
    search_fields = ('community', 'user')
    list_filter = ('created_at', 'updated_at')


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'community', 'title', 'content', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')

@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'vote', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'parent', 'is_deleted', 'content', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')

