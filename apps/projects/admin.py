from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'is_deleted')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_deleted', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
