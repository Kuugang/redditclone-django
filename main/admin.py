from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'birth_date', 'avatar', 'bio', 'updated_at')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, UserAdmin)

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
    list_display = ('id', 'community', 'rule', 'created_at', 'updated_at')
    search_fields = ('community', 'rule')
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

