from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


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
