from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from git.models import Project, Milestone, Issue

TEST_TITLE = 'Test Title'
TEST_DESCRIPTION = 'Test Description'
TEST_GIT_REPO = 'http://github.com/test'
TEST_USER_USERNAME = 'testUser'
TEST_USER_EMAIL = 'testUser@test.com'
TEST_USER_PASSWORD = 'testing321'


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

        self.test_project = Project.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            git_repo=TEST_GIT_REPO,
            date_created=timezone.now(),
            owner=self.test_user)

    def test_title_label(self):
        field_label = self.test_project._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        field_label = self.test_project._meta.get_field(
            'description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_git_repo_label(self):
        field_label = self.test_project._meta.get_field(
            'git_repo').verbose_name
        self.assertEqual(field_label, 'git repo')

    def test_date_created_label(self):
        field_label = self.test_project._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_owner_label(self):
        field_label = self.test_project._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'owner')

    def test_collaborators_label(self):
        field_label = self.test_project._meta.get_field(
            'collaborators').verbose_name
        self.assertEqual(field_label, 'collaborators')

    def test_title_max_length(self):
        max_length = self.test_project._meta.get_field('title').max_length
        self.assertEqual(max_length, 32)

    def test_description_max_length(self):
        max_length = self.test_project._meta.get_field(
            'description').max_length
        self.assertEqual(max_length, 100)

    def test_git_repo_max_length(self):
        max_length = self.test_project._meta.get_field('git_repo').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_title(self):
        expected_object_name = f'{self.test_project.title}'
        self.assertEqual(str(self.test_project), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.test_project.get_absolute_url(),
                         f'/project/{self.test_project.id}/')


class MilestoneModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

        self.test_project = Project.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            git_repo=TEST_GIT_REPO,
            date_created=timezone.now(),
            owner=self.test_user)

        self.test_milestone = Milestone.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            project=self.test_project)

    def test_title_label(self):
        milestone = Milestone.objects.get(id=1)
        field_label = milestone._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        milestone = Milestone.objects.get(id=1)
        field_label = milestone._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_due_date_label(self):
        milestone = Milestone.objects.get(id=1)
        field_label = milestone._meta.get_field('due_date').verbose_name
        self.assertEqual(field_label, 'due date')

    def test_is_open_label(self):
        milestone = Milestone.objects.get(id=1)
        field_label = milestone._meta.get_field('is_open').verbose_name
        self.assertEqual(field_label, 'is open')

    def test_project_label(self):
        milestone = Milestone.objects.get(id=1)
        field_label = milestone._meta.get_field('project').verbose_name
        self.assertEqual(field_label, 'project')

    def test_title_max_length(self):
        milestone = Milestone.objects.get(id=1)
        max_length = milestone._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_max_length(self):
        milestone = Milestone.objects.get(id=1)
        max_length = milestone._meta.get_field('description').max_length
        self.assertEqual(max_length, 300)

    def test_object_name_is_title(self):
        milestone = Milestone.objects.get(id=1)
        expected_object_name = f'{milestone.title}'
        self.assertEqual(str(milestone), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.test_project.get_absolute_url(),
                         f'/project/{self.test_project.id}/')


class IssueModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

        self.test_project = Project.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            git_repo=TEST_GIT_REPO,
            date_created=timezone.now(),
            owner=self.test_user)

        self.test_issue = Issue.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            project=self.test_project,
            author=self.test_user
        )

    def test_title_label(self):
        field_label = self.test_issue._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        field_label = self.test_issue._meta.get_field(
            'description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_author_label(self):
        field_label = self.test_issue._meta.get_field(
            'author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_date_created_label(self):
        field_label = self.test_issue._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_date_closed_label(self):
        field_label = self.test_issue._meta.get_field(
            'date_closed').verbose_name
        self.assertEqual(field_label, 'date closed')

    def test_is_open_label(self):
        field_label = self.test_issue._meta.get_field('is_open').verbose_name
        self.assertEqual(field_label, 'is open')

    def test_project_label(self):
        field_label = self.test_issue._meta.get_field('project').verbose_name
        self.assertEqual(field_label, 'project')

    def test_title_max_length(self):
        max_length = self.test_issue._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_description_max_length(self):
        max_length = self.test_issue._meta.get_field(
            'description').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_title(self):
        expected_object_name = f'{self.test_issue.title}'
        self.assertEqual(str(self.test_issue), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.test_issue.get_absolute_url(),
                         f'/project/{self.test_issue.id}/')
