from django.contrib.auth.models import User
from django.db import models

# Create your models here.
GENERAL_STATES = (
    ('OPEN', 'Open'),
    ('CLOSE', 'Close'),
    ('MERGED', 'Merged')
)

class Project(models.Model):
    title = models.CharField(max_length=32)
    contributors = models.ManyToManyField(User)
    git_repo = models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.title)

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
