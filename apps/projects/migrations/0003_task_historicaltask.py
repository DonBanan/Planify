# Generated by Django 4.2.13 on 2024-06-29 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_alter_project_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Is Completed')),
                ('status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('archived', 'Archived')], default='new', max_length=20, verbose_name='Status')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10, verbose_name='Priority')),
                ('archived_at', models.DateTimeField(blank=True, null=True, verbose_name='Archived At')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTask',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Updated At')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Is Completed')),
                ('status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('archived', 'Archived')], default='new', max_length=20, verbose_name='Status')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10, verbose_name='Priority')),
                ('archived_at', models.DateTimeField(blank=True, null=True, verbose_name='Archived At')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'historical Task',
                'verbose_name_plural': 'historical Tasks',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
