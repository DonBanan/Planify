from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Project(models.Model):
    title = models.CharField(_('Title'), max_length=256, unique=True)
    slug = models.SlugField(_('Slug'), max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    is_deleted = models.BooleanField(_('Is Deleted'), default=False)

    objects = ProjectManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title


class Column(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name=_("Title"))
    project = models.ForeignKey(Project, related_name='columns', on_delete=models.CASCADE, verbose_name=_("Project"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        ordering = ['created_at']

    def __str__(self):
        return self.title


class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived_at__isnull=True)


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('archived', _('Archived')),
    ]
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]

    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    due_date = models.DateField(_('Due Date'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    is_completed = models.BooleanField(_('Is Completed'), default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Project'))
    column = models.ForeignKey(Column, related_name='column_tasks', on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name=_("Column"))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(_('Priority'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    history = HistoricalRecords()

    archived_at = models.DateTimeField(_('Archived At'), blank=True, null=True)

    objects = models.Manager()
    active_tasks = TaskManager()

    def archive(self):
        self.status = 'archived'
        self.archived_at = timezone.now()
        self.save()

    def unarchive(self):
        self.status = 'new'
        self.archived_at = None
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
