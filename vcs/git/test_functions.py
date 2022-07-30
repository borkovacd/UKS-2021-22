from .utils import request_passes_test
from .models import (
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
    if request.user == issue.author:
        return True
    if request.user in issue.assignees.all():
        return True
    return False
