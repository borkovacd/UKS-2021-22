from msilib.schema import ListView
from pydoc import describe
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView
)
from django.contrib import messages
from .models import Milestone, GENERAL_STATES, Project


def home(request):
    return render(request, 'git/home.html')


def milestones(request, project_id):
    objects = Milestone.objects.all().filter(project=project_id)
    template = loader.get_template('git/milestones.html')
    context = {
        'milestones': objects,
        'project_id': project_id
    }
    return HttpResponse(template.render(context, request))


def milestone_form(request, project_id):
    template = loader.get_template('git/milestone-form.html')
    milestone = ''
    context = {
        'milestone': milestone,
        'project_id': project_id
    }
    return HttpResponse(template.render(context, request))


def new_milestone(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        milestone = Milestone.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date'],
            state='OPEN',
            project=project
        )
        milestone.save()
        messages.success(
            request, f'The milestone "{milestone.title}" was added successfully!')
        return redirect(reverse('project-detail', args=[project_id], ))
    else:
        project_id = request.path.split('/')[-1]
        template = loader.get_template('git/milestone-form.html')
        context = {'project_id': project_id}
        return HttpResponse(template.render(context, request))


def delete_milestone(request, milestone_id, project_id):
    if request.method == 'POST':
        milestone = Milestone.objects.get(id=milestone_id)
        milestone.delete()
        return HttpResponseRedirect(reverse('milestones', kwargs={'project_id': project_id}))


def project_form(request):
    template = loader.get_template('git/project-form.html')
    project = ''
    context = {
        'project': project
    }
    return HttpResponse(template.render(context, request))


def new_project(request):
    if request.method == 'POST':
        project = Project.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            git_repo=request.POST['git_repo'],
            owner=request.user
        )
        project.save()
        messages.success(
            request, f'The project "{project.title}" was added successfully!')
    else:
        template = loader.get_template('vcs/new_project.html')
        context = {}
        return HttpResponse(template.render(context, request))
    return HttpResponseRedirect(project.get_absolute_url())

# class based PROJECTS view


class ProjectListView(ListView):
    model = Project
    template_name = 'git/home.html'  # <app>/<model>_<viewtype>.html
    # by default it expects this: git/project_list.html
    context_object_name = 'projects'

# function based PROJECTS view


def projects(request):
    projects = Project.objects.all()
    template = loader.get_template('git/projects.html')
    context = {
        'projects': projects,
    }
    return HttpResponse(template.render(context, request))


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['milestones'] = Milestone.objects.filter(
            project_id=self.object)

        return context
