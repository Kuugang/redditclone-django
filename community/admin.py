from django.contrib import admin
from .models import Community, CommunityMember, CommunityPostReport, CommunityEventParticipant
# Register your models here.

admin.site.register(CommunityMember)
admin.site.register(CommunityPostReport)
admin.site.register(CommunityEventParticipant)
@admin.register(Community)

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'visibility', 'about', 'avatar', 'banner', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')