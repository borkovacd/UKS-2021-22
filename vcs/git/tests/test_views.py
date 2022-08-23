
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from git.models import Milestone, Project, Issue
from colorfield.fields import ColorField
from colorful.fields import RGBColorField


TEST_TITLE = 'Test Title'
TEST_DESCRIPTION = 'Test Description'
TEST_GIT_REPO = 'http://github.com/test'
TEST_USER_USERNAME = 'testUser'
TEST_USER_EMAIL = 'testUser@test.com'
TEST_USER_PASSWORD = 'testing321'

# PROJECTS


class ProjectCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        testUser = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('project-create'))
        self.assertRedirects(response, '/login/?next=/new-project/')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.get('/new-project/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.get(reverse('project-create'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testUser')

        # Check we used correct template
        self.assertTemplateUsed(response, 'git/project_form.html')

    def test_when_valid_data_then_project_created_successfully(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.post(
            reverse('project-create'),
            {
                'title': TEST_TITLE,
                'description': TEST_DESCRIPTION,
                'git_repo': TEST_GIT_REPO})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.last().title, TEST_TITLE)
        self.assertEqual(Project.objects.last().description, TEST_DESCRIPTION)
        self.assertEqual(Project.objects.last().git_repo, TEST_GIT_REPO)
        self.assertEqual(
            Project.objects.last().owner.username, TEST_USER_USERNAME)

    def test_when_no_title_given_then_project_not_created(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.post(
            reverse('project-create'),
            {
                'description': TEST_DESCRIPTION,
                'git_repo': TEST_GIT_REPO})
        self.assertEqual(Project.objects.all().count(), 0)

    def test_when_no_git_repo_given_then_project_not_created(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.post(
            reverse('project-create'),
            {
                'title': TEST_TITLE,
                'description': TEST_DESCRIPTION})
        self.assertEqual(Project.objects.all().count(), 0)

    def test_when_no_description_given_then_project_created_successfully(self):
        login = self.client.login(
            username='testUser', password='testing321')
        response = self.client.post(
            reverse('project-create'),
            {
                'title': TEST_TITLE,
                'git_repo': TEST_GIT_REPO})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.last().title, TEST_TITLE)
        self.assertEqual(Project.objects.last().git_repo, TEST_GIT_REPO)
        self.assertEqual(
            Project.objects.last().owner.username, TEST_USER_USERNAME)


class ProjectUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

        self.project = Project.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            git_repo=TEST_GIT_REPO,
            date_created=timezone.now(),
            owner=self.test_user)

        User.objects.create_user(
            username=TEST_USER_USERNAME+'2',
            email='testUser2@test.com',
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('project-update', args=[self.project.id]))
        self.assertRedirects(
            response, f'/login/?next=/project/{self.project.id}/update/')

    def test_view_forbidden_if_user_not_owner(self):
        login = self.client.login(
            username=TEST_USER_USERNAME+'2', password=TEST_USER_PASSWORD)
        response = self.client.get(f'/project/{self.project.id}/update/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(f'/project/{self.project.id}/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('project-update', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('project-update', args=[self.project.id]))
        self.assertTemplateUsed(response, 'git/project_form.html')

    def test_when_valid_data_then_project_updated_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('project-update', args=[self.project.id]),
            {
                'title': TEST_TITLE+'updated',
                'description': TEST_DESCRIPTION+'updated',
                'git_repo': TEST_GIT_REPO+'updated'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.last().title, TEST_TITLE+'updated')
        self.assertEqual(Project.objects.last().description,
                         TEST_DESCRIPTION+'updated')
        self.assertEqual(Project.objects.last().git_repo,
                         TEST_GIT_REPO+'updated')
        self.assertEqual(
            Project.objects.last().owner.username, TEST_USER_USERNAME)

    def test_when_only_title_changed_then_project_title_updated(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('project-update', args=[self.project.id]),
            {
                'title': TEST_TITLE+'updated',
                'description': TEST_DESCRIPTION,
                'git_repo': TEST_GIT_REPO
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.last().title, TEST_TITLE+'updated')
        self.assertEqual(Project.objects.last().description,
                         TEST_DESCRIPTION)
        self.assertEqual(Project.objects.last().git_repo,
                         TEST_GIT_REPO)
        self.assertEqual(
            Project.objects.last().owner.username, TEST_USER_USERNAME)

    def test_when_only_description_changed_then_project_description_updated(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('project-update', args=[self.project.id]),
            {
                'title': TEST_TITLE,
                'description': TEST_DESCRIPTION+'updated',
                'git_repo': TEST_GIT_REPO
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.last().title, TEST_TITLE)
        self.assertEqual(Project.objects.last().description,
                         TEST_DESCRIPTION+'updated')
        self.assertEqual(Project.objects.last().git_repo,
                         TEST_GIT_REPO)
        self.assertEqual(
            Project.objects.last().owner.username, TEST_USER_USERNAME)

    def test_when_only_git_repo_changed_then_project_repo_updated(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('project-update', args=[self.project.id]),
            {
                'title': TEST_TITLE,
                'description': TEST_DESCRIPTION,
                'git_repo': TEST_GIT_REPO+'updated'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.last().title, TEST_TITLE)
        self.assertEqual(Project.objects.last().description,
                         TEST_DESCRIPTION)
        self.assertEqual(Project.objects.last().git_repo,
                         TEST_GIT_REPO+'updated')
        self.assertEqual(
            Project.objects.last().owner.username, TEST_USER_USERNAME)


class ProjectDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

        self.project = Project.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            git_repo=TEST_GIT_REPO,
            date_created=timezone.now(),
            owner=self.test_user)

        User.objects.create_user(
            username=TEST_USER_USERNAME+'2',
            email='testUser2@test.com',
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('project-delete', args=[self.project.id]))
        self.assertRedirects(
            response, f'/login/?next=/project/{self.project.id}/delete/')

    def test_view_forbidden_if_user_not_owner(self):
        login = self.client.login(
            username=TEST_USER_USERNAME+'2', password=TEST_USER_PASSWORD)
        response = self.client.get(f'/project/{self.project.id}/delete/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(f'/project/{self.project.id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('project-delete', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('project-delete', args=[self.project.id]))
        self.assertTemplateUsed(response, 'git/project_confirm_delete.html')

    def test_when_valid_id_and_user_then_project_deleted_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('project-delete', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.all().count(), 0)

    def test_when_invalid_project_id_then_project_not_found_error(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('project-delete', args=[self.project.id+1]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Project.objects.all().count(), 1)


class ProjectListViewTest(TestCase):
    @ classmethod
    def setUpTestData(cls):
        testUser = User.objects.create_user(
            username='testUser',
            email='testUser@test.com',
            password='testing321')

        number_of_projects = 3

        for project_id in range(number_of_projects):
            Project.objects.create(
                title=f'Test Project Title {project_id}',
                description=f'Test Project Description {project_id}',
                git_repo=f'http://github.com/test{project_id}',
                date_created=timezone.now(),
                owner=testUser)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('git-home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('git-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'git/home.html')

    def test_lists_all_projects(self):
        response = self.client.get(reverse('git-home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['projects']), 3)

# MILESTONES


class MilestoneCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user = User.objects.create_user(
            username=TEST_USER_USERNAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD)

        self.project = Project.objects.create(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            git_repo=TEST_GIT_REPO,
            date_created=timezone.now(),
            owner=self.test_user)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('milestone-create', args=[self.project.id]))
        self.assertRedirects(
            response, f'/login/?next=/project/{self.project.id}/new-milestone/')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/project/{self.project.id}/new-milestone/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('milestone-create', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('milestone-create', args=[self.project.id]))
        self.assertTemplateUsed(response, 'git/milestone_form.html')

    def test_given_valid_data_then_milestone_created_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('milestone-create', args=[self.project.id]),
            {
                'title': TEST_TITLE,
                'description': TEST_DESCRIPTION,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Milestone.objects.all().count(), 1)
        self.assertEqual(Milestone.objects.last().title, TEST_TITLE)
        self.assertEqual(Milestone.objects.last().description,
                         TEST_DESCRIPTION)
        self.assertTrue(Milestone.objects.last().is_open)
        self.assertEqual(
            Milestone.objects.last().project.id, self.project.id)

    def test_given_only_title_then_milestone_created_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('milestone-create', args=[self.project.id]),
            {
                'title': TEST_TITLE
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Milestone.objects.all().count(), 1)
        self.assertEqual(Milestone.objects.last().title, TEST_TITLE)
        self.assertTrue(Milestone.objects.last().is_open)
        self.assertEqual(
            Milestone.objects.last().project.id, self.project.id)

    def test_given_no_title_then_milestone_not_created(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('milestone-create', args=[self.project.id]),
            {
                'description': TEST_DESCRIPTION
            })
        self.assertEqual(Milestone.objects.all().count(), 0)


class MilestoneUpdateViewTest(TestCase):

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
            project=self.test_project
        )

        User.objects.create_user(
            username=TEST_USER_USERNAME+'2',
            email='testUser2@test.com',
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('milestone-update', args=[self.test_milestone.id]))
        self.assertRedirects(
            response, f'/login/?next=/milestones/{self.test_milestone.id}/update/')

    def test_view_forbidden_if_user_not_owner(self):
        login = self.client.login(
            username=TEST_USER_USERNAME+'2', password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/milestones/{self.test_milestone.id}/update/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/milestones/{self.test_milestone.id}/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('milestone-update', args=[self.test_milestone.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('milestone-update', args=[self.test_milestone.id]))
        self.assertTemplateUsed(response, 'git/milestone_form.html')

    def test_when_valid_data_then_project_updated_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('milestone-update', args=[self.test_milestone.id]),
            {
                'title': TEST_TITLE+'updated',
                'description': TEST_DESCRIPTION+'updated'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Milestone.objects.all().count(), 1)
        self.assertEqual(Milestone.objects.last().title, TEST_TITLE+'updated')
        self.assertEqual(Milestone.objects.last().description,
                         TEST_DESCRIPTION+'updated')
        self.assertEqual(
            Milestone.objects.last().project.id, self.test_project.id)


class MilestoneDeleteViewTest(TestCase):
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
            project=self.test_project
        )

        User.objects.create_user(
            username=TEST_USER_USERNAME+'2',
            email='testUser2@test.com',
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('milestone-delete', args=[self.test_milestone.id]))
        self.assertRedirects(
            response, f'/login/?next=/milestones/{self.test_milestone.id}/delete/')

    def test_view_forbidden_if_user_not_owner(self):
        login = self.client.login(
            username=TEST_USER_USERNAME+'2', password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/milestones/{self.test_milestone.id}/delete/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/milestones/{self.test_milestone.id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('milestone-delete', args=[self.test_milestone.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('milestone-delete', args=[self.test_milestone.id]))
        self.assertTemplateUsed(response, 'git/milestone_confirm_delete.html')

    def test_when_valid_id_and_user_then_project_deleted_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('milestone-delete', args=[self.test_milestone.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Milestone.objects.all().count(), 0)


class IssueCreateViewTest(TestCase):
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('issue-create', args=[self.test_project.id]))
        self.assertRedirects(
            response, f'/login/?next=/project/{self.test_project.id}/new-issue/')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/project/{self.test_project.id}/new-issue/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('issue-create', args=[self.test_project.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('issue-create', args=[self.test_project.id]))
        self.assertTemplateUsed(response, 'git/issue_form.html')

    def test_given_valid_data_then_issue_created_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('issue-create', args=[self.test_project.id]),
            {
                'title': TEST_TITLE,
                'description': TEST_DESCRIPTION,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Issue.objects.all().count(), 1)
        self.assertEqual(Issue.objects.last().title, TEST_TITLE)
        self.assertEqual(Issue.objects.last().description,
                         TEST_DESCRIPTION)
        self.assertTrue(Issue.objects.last().is_open)
        self.assertEqual(
            Issue.objects.last().project.id, self.test_project.id)
        self.assertEqual(
            Issue.objects.last().author.username, TEST_USER_USERNAME)

    def test_given_only_title_then_issue_created_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('issue-create', args=[self.test_project.id]),
            {
                'title': TEST_TITLE
            })
        self.assertEqual(Issue.objects.all().count(), 1)
        self.assertEqual(Issue.objects.last().title, TEST_TITLE)
        self.assertTrue(Issue.objects.last().is_open)
        self.assertEqual(
            Issue.objects.last().project.id, self.test_project.id)
        self.assertEqual(
            Issue.objects.last().author.username, TEST_USER_USERNAME)

    def test_given_no_title_then_issue_not_created(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('issue-create', args=[self.test_project.id]),
            {
                'description': TEST_DESCRIPTION
            })
        self.assertEqual(Issue.objects.all().count(), 0)


class IssueUpdateViewTest(TestCase):

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

        User.objects.create_user(
            username=TEST_USER_USERNAME+'2',
            email='testUser2@test.com',
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('issue-update', args=[self.test_issue.id]))
        self.assertRedirects(
            response, f'/login/?next=/issues/{self.test_issue.id}/update/')

    def test_view_forbidden_if_user_not_owner(self):
        login = self.client.login(
            username=TEST_USER_USERNAME+'2', password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/issues/{self.test_issue.id}/update/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/issues/{self.test_issue.id}/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('issue-update', args=[self.test_issue.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('issue-update', args=[self.test_issue.id]))
        self.assertTemplateUsed(response, 'git/issue_form.html')

    def test_when_valid_data_then_project_updated_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('issue-update', args=[self.test_issue.id]),
            {
                'title': TEST_TITLE+'updated',
                'description': TEST_DESCRIPTION+'updated'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Issue.objects.all().count(), 1)
        self.assertEqual(Issue.objects.last().title, TEST_TITLE+'updated')
        self.assertEqual(Issue.objects.last().description,
                         TEST_DESCRIPTION+'updated')
        self.assertEqual(
            Issue.objects.last().project.id, self.test_project.id)
        self.assertEqual(
            Issue.objects.last().author.username, TEST_USER_USERNAME)


class IssueDeleteViewTest(TestCase):
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

        User.objects.create_user(
            username=TEST_USER_USERNAME+'2',
            email='testUser2@test.com',
            password=TEST_USER_PASSWORD)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('issue-delete', args=[self.test_issue.id]))
        self.assertRedirects(
            response, f'/login/?next=/issues/{self.test_issue.id}/delete/')

    def test_view_forbidden_if_user_not_owner(self):
        login = self.client.login(
            username=TEST_USER_USERNAME+'2', password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/issues/{self.test_issue.id}/delete/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            f'/issues/{self.test_issue.id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('issue-delete', args=[self.test_issue.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(
            reverse('issue-delete', args=[self.test_issue.id]))
        self.assertTemplateUsed(response, 'git/issue_confirm_delete.html')

    def test_when_valid_id_and_user_then_project_deleted_successfully(self):
        login = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(
            reverse('issue-delete', args=[self.test_issue.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Issue.objects.all().count(), 0)
