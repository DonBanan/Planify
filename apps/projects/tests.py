from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from .models import Project


class ProjectTestCase(TestCase):

    def setUp(self):
        # Created several projects for testing
        self.project1 = Project.objects.create(title="Active Project 1")
        self.project2 = Project.objects.create(title="Active Project 2")
        self.project3 = Project.objects.create(title="Deleted Project", is_deleted=True)

    def test_create_project(self):
        # Checking the project creations (there are 6 in total)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(self.project1.title, "Active Project 1")

    def test_delete_project(self):
        # Check the deletions of the project marked as is_deleted (there will be 5 of them in total)
        self.project1.delete()
        self.assertTrue(self.project1.is_deleted)
        self.assertEqual(Project.objects.filter(is_deleted=False).count(), 1)

    def test_project_manager_filter_not_deleted(self):
        # I check the manager for filtering no deleted projects (there should be 5 in total)
        active_projects = Project.objects.all()
        self.assertEqual(active_projects.count(), 2)
        self.assertIn(self.project1, active_projects)
        self.assertIn(self.project2, active_projects)
        self.assertNotIn(self.project3, active_projects)
