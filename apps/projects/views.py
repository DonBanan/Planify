from rest_framework import permissions, viewsets

from .models import Project, Column, Task
from .serializers import ProjectSerializer, ColumnSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ColumnViewSet(viewsets.ModelViewSet):
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_slug = self.kwargs.get('project_slug')
        return Column.objects.filter(project__slug=project_slug)

    def perform_create(self, serializer):
        project_slug = self.kwargs.get('project_slug')
        project = Project.objects.get(slug=project_slug)
        serializer.save(project=project)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_slug = self.kwargs.get('project_slug')
        return Task.objects.filter(project__slug=project_slug)

    def perform_create(self, serializer):
        project_slug = self.kwargs.get('project_slug')
        project = Project.objects.get(slug=project_slug)
        serializer.save(project=project)