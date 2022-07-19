from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from colorfield.fields import ColorField
from colorful.fields import RGBColorField
from enum import Enum

# Create your models here.
GENERAL_STATES = (
    ('OPEN', 'Open'),
    ('CLOSE', 'Close'),
    ('MERGED', 'Merged')
)


class Issue_State(Enum):
    OPEN = 1
    CLOSED = 2


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
    due_date = models.DateTimeField()
    description = models.TextField(max_length=300, blank=True)
    state = models.CharField(
        max_length=6,
        choices=GENERAL_STATES,
        default='OPEN',
    )
    project = models.ForeignKey(Project, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


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
        Milestone, on_delete=models.CASCADE, blank=True)
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
