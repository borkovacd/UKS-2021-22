from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import Project, Commit
from datetime import datetime


@csrf_exempt
def webhook_push(request):
    try:
        body_string = request.body.decode("utf-8")
        json_data = json.loads(body_string)
        commits = json_data['commits']
        project_url = json_data["repository"]["html_url"]
        project = Project.objects.get(git_repo=project_url)

        if project:
            for commit in commits:
                commit_url = commit["url"]
                message = commit["message"]
                author = commit["committer"]
                date_created = commit["timestamp"]
                new_time = datetime.strptime(
                    date_created, "%Y-%m-%dT%H:%M:%S%z")
                new_time_django = datetime(
                    new_time.year, new_time.month, new_time.day, new_time.hour, new_time.minute, new_time.second)
                commit_id = commit["id"]
                new_commit = Commit.create(commit_url, commit_id, message, new_time_django,
                                           author["username"], project)

        return HttpResponse('Webhook infromation received successfully')
    except:
        return HttpResponse('Exception occured while parsing webhook data')
