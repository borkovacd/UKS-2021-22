from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from colorfield.fields import ColorField
from colorful.fields import RGBColorField
from enum import Enum


class Project(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=100, blank=True)
    git_repo = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    # if the user us deleted, delete the project too
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects')
    collaborators = models.ManyToManyField(User)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class Milestone(models.Model):
    title = models.CharField(max_length=200, blank=False)
    due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=300, blank=True)
    is_open = models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.pk})


class Label(models.Model):
    title = models.CharField(max_length=50)
    color = RGBColorField()
    description = models.CharField(max_length=100, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.project.pk})


class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_closed = models.DateTimeField(null=True)
    is_open = models.BooleanField(default=True)
    milestone = models.ForeignKey(
        Milestone, on_delete=models.SET_NULL, blank=True, null=True)
    labels = models.ManyToManyField(Label, blank=True)
    assignees = models.ManyToManyField(
        User, related_name='assignees', blank=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.project.pk})


class Comment(models.Model):
    text = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_edited = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.text)

    def get_absolute_url(self):
        return reverse("issue-detail", kwargs={"pk": self.issue.pk})


class Commit(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    url = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @classmethod
    def create(cls, commit_url, commit_id, message, date_created, author, project):
        new_state = cls(url=commit_url, id=commit_id, message=message, date_created=date_created,
                        author=author, project=project)
        new_state.save()
        return new_state

    def __str__(self):
        return str(self.message)

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.project.pk})
