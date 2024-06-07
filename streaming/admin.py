from django.contrib import admin

from .models import StreamingSetting

@admin.register(StreamingSetting)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'num_cam', 'date_joined')
    list_filter = ('date_joined', 'num_cam')
    search_fields = ('start', 'channel_name')


