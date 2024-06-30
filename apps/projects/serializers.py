from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'title', 'slug', 'tasks_count')

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        if 'request' in self.context:
            kwargs['tasks_url'] = {
                'view_name': 'project-tasks-list',
                'lookup_url_kwarg': 'slug',
                'lookup_field': 'slug',
            }
        return kwargs


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'created_at', 'updated_at',
                  'is_completed', 'status', 'priority', 'archived_at', 'project')

    def create(self, validated_data):
        project_data = validated_data.pop('project')
        project = Project.objects.create(**project_data)
        task = Task.objects.create(project=project, **validated_data)
        return task

    def update(self, instance, validated_data):
        project_data = validated_data.pop('project')
        instance.project.title = project_data.get('title', instance.project.title)
        instance.project.save()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.archived_at = validated_data.get('archived_at', instance.archived_at)
        instance.save()
        return instance