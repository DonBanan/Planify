from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Project, Column, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'is_deleted')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_deleted', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_at', 'updated_at')
    list_filter = ('project',)
    search_fields = ('title', 'project__title')
    ordering = ('-created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'column', 'status', 'priority', 'due_date', 'is_completed')
    list_filter = ('project', 'column', 'status', 'priority', 'is_completed')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    actions = ['archive_tasks', 'unarchive_tasks']

    def archive_tasks(self, request, queryset):
        queryset.update(status='archived', archived_at=timezone.now())

    def unarchive_tasks(self, request, queryset):
        queryset.update(status='new', archived_at=None)

    archive_tasks.short_description = _("Archive selected tasks")
    unarchive_tasks.short_description = _("Unarchive selected tasks")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(archived_at__isnull=True)
