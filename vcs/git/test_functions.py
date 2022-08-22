from .utils import request_passes_test
from .models import (
    Milestone,
    Project,
    Issue
)


@request_passes_test
def test_ownership(request, **kwargs):
    project = Project.objects.get(id=kwargs['project_id'])
    if request.user == project.owner:
        return True
    return False


@request_passes_test
def test_issue_permissions(request, **kwargs):
    issue = Issue.objects.get(id=kwargs['issue_id'])
    project = issue.project
    if request.user == project.owner:
        return True
    if request.user in project.collaborators.all():
        return True
    return False


@request_passes_test
def test_milestone_permissions(request, **kwargs):
    milestone = Milestone.objects.get(id=kwargs['milestone_id'])
    project = milestone.project
    if request.user == project.owner:
        return True
    if request.user in project.collaborators.all():
        return True
    return False
