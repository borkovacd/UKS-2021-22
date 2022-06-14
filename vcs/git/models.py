from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
GENERAL_STATES = (
    ('OPEN', 'Open'),
    ('CLOSE', 'Close'),
    ('MERGED', 'Merged')
)


class Project(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
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
