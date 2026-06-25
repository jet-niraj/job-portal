from django.contrib import admin
from django.utils.html import format_html
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'job_title',
        'status_badge',
        'category',
        'city',
        'state',
        'start_date',
        'created_at'
    ]
    
    list_filter = ['status', 'category', 'city', 'state', 'created_at']
    search_fields = ['job_title', 'description', 'city', 'state']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Job Information', {
            'fields': ('job_title', 'description', 'status', 'category')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date')
        }),
        ('Media', {
            'fields': ('job_profile_picture', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    def status_badge(self, obj):
        """
        Display status as a colored badge
        """
        colors = {
            'draft': '#808080',
            'requested': '#FFA500',
            'posted': '#0066CC',
            'filled': '#00AA00',
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def image_preview(self, obj):
        """
        Display image preview in admin
        """
        if obj.job_profile_picture:
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 5px;" />',
                obj.job_profile_picture.url
            )
        return 'No image'
    image_preview.short_description = 'Image Preview'