from django.contrib import admin
from .models import Comment, Post, UserSavedPost

# Register your models here.
admin.site.register(Comment)
admin.site.register(UserSavedPost)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'user', 'community', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
