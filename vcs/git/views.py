from cProfile import label
from msilib.schema import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import (
    Commit,
    Project,
    Issue,
    Milestone,
    Label,
    Comment
)
from .forms import (
    CollaboratorsForm,
    IssueForm,
    LabelForm,
    CommentForm,
    MilestoneForm
)
from django.contrib.auth.models import User
from django.db.models import Q
from .test_functions import (
    test_ownership,
    test_issue_permissions,
    test_milestone_permissions
)
from django.views.generic.edit import FormMixin


def home(request):
    return render(request, 'git/home.html')

# MILESTONES


def milestones(request, project_id):
    objects = Milestone.objects.all().filter(project=project_id)
    template = loader.get_template('git/milestones.html')
    context = {
        'milestones': objects,
        'project_id': project_id
    }
    return HttpResponse(template.render(context, request))


class MilestoneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Milestone
    form_class = MilestoneForm

    def form_valid(self, form):
        form.instance.project = Project.objects.get(
            id=self.kwargs['project_id'])
        milestone_title = form.cleaned_data['title']
        messages.success(
            self.request, f'The milestone "{milestone_title}" was created successfully!')
        return super().form_valid(form)

    def test_func(self):
        project = Project.objects.get(
            id=self.kwargs['project_id'])
        if self.request.user == project.owner:
            return True
        if self.request.user in project.collaborators.all():
            return True
        return False


class MilestoneDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Milestone

    def get_success_url(self):
        project = self.object.project
        messages.success(
            self.request, f'The milestone "{self.object.title}" was removed successfully!')
        return reverse('project-detail', args=[project.id])

    def test_func(self):
        milestone = Milestone.objects.get(
            id=self.kwargs['pk'])
        project = milestone.project
        if self.request.user == project.owner:
            return True
        if self.request.user in project.collaborators.all():
            return True
        return False


class MilestoneUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Milestone
    form_class = MilestoneForm

    def form_valid(self, form):
        milestone_title = form.cleaned_data['title']
        messages.success(
            self.request, f'The milestone "{milestone_title}" was updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        milestone = Milestone.objects.get(
            id=self.kwargs['pk'])
        project = milestone.project
        if self.request.user == project.owner:
            return True
        if self.request.user in project.collaborators.all():
            return True
        return False


def project_form(request):
    template = loader.get_template('git/project_form.html')
    project = ''
    context = {
        'project': project
    }
    return HttpResponse(template.render(context, request))


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'description', 'git_repo']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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
        context['labels'] = Label.objects.filter(
            project_id=self.object)
        context['issues'] = Issue.objects.filter(
            project_id=self.object)
        context['commits'] = Commit.objects.filter(
            project_id=self.object)

        return context


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'git_repo']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.owner:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.owner:
            return True
        return False


### COLLABORATORS ###


def collaborators(request, project_id):
    projects = Project.objects.all().filter(project=project_id)
    template = loader.get_template('git/collaborators.html')
    context = {
        'projects': projects,
        'project_id': project_id
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_collaborator(request, project_id):
    project = Project.objects.get(id=project_id)
    exisitingCollaborators = project.collaborators.all()
    form = CollaboratorsForm(
        request.user.id, exisitingCollaborators, request.POST)
    if request.method == 'POST':
        collaborators = [*exisitingCollaborators,
                         *request.POST.getlist('collaborators')]
        project.collaborators.set(collaborators)
        project.save()
        messages.success(
            request, f'The collaborators ware saved successfully!')
    else:
        return render(
            request,
            'git/collaborator_form.html',
            {
                'form': form,
                'project': project
            })
    return HttpResponseRedirect(project.get_absolute_url())


@login_required
def delete_collaborator(request, project_id, collaborator_id):
    collaborator = User.objects.get(id=collaborator_id)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.collaborators.remove(collaborator_id)
        project.save()
        messages.success(
            request, f'The collaborator "{collaborator.username}" was removed successfully!')
        return redirect(reverse('project-detail', args=[project_id]))
    else:
        return render(
            request,
            'git/collaborator_confirm_delete.html',
            {
                'collaborator': collaborator,
                'project': project
            }
        )

# LABELS


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['title', 'color', 'description']

    def form_valid(self, form):
        form.instance.project = Project.objects.get(
            id=self.kwargs['project_id'])
        label_title = form.cleaned_data['title']
        messages.success(
            self.request, f'The label "{label_title}" was created successfully!')
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label

    def get_success_url(self):
        project = self.object.project
        messages.success(
            self.request, f'The label "{self.object.title}" was removed successfully!')
        return reverse('project-detail', args=[project.id])


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm

    def form_valid(self, form):
        label_title = form.cleaned_data['title']
        messages.success(
            self.request, f'The label "{label_title}" was updated successfully!')
        return super().form_valid(form)


# ISSUES


@login_required
@test_ownership
def add_issue(request, project_id):
    form = IssueForm(request.POST)
    form.fields['milestone'].queryset = Milestone.objects.filter(
        project_id=project_id)
    form.fields['labels'].queryset = Label.objects.filter(
        project_id=project_id)
    form.fields['assignees'].queryset = User.objects.filter(is_superuser=False).filter(
        ~Q(id=request.user.id))
    if request.method == 'POST':
        if form.is_valid():
            new_issue = form.instance
            new_issue.author_id = request.user.id
            new_issue.project_id = project_id
            new_issue.save()
            new_issue.labels.set(form.cleaned_data['labels'])
            new_issue.assignees.set(form.cleaned_data['assignees'])
            new_issue.save()
            issue_title = form.cleaned_data['title']
            messages.success(
                request, f'The issue "{issue_title}" was created successfully!')
            return redirect(reverse('project-detail', args=[project_id]))
    return render(request, 'git/issue_form.html', {'form': form})


class IssueDetailView(FormMixin, DetailView):
    model = Issue
    context_object_name = 'comment'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(issue_id=self.object.pk)
        context['form'] = self.get_form()
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        new_comment = form.instance
        new_comment.author_id = request.user.id
        new_comment.issue_id = self.object.pk
        new_comment.text = form['text'].value()
        new_comment.save()
        return super(IssueDetailView, self).form_valid(form)


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue

    def get_success_url(self):
        project = self.object.project
        messages.success(
            self.request, f'The issue "{self.object.title}" was removed successfully!')
        return reverse('project-detail', args=[project.id])

    def test_func(self):
        issue = self.get_object()
        if self.request.user == issue.author:
            return True
        return False


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['title', 'description']

    def form_valid(self, form):
        issue_title = form.cleaned_data['title']
        messages.success(
            self.request, f'The issue "{issue_title}" was updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        issue = self.get_object()
        if self.request.user == issue.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        issue = self.object.issue
        messages.success(
            self.request, f'The comment "{self.object.text}" was removed successfully!')
        return reverse('issue-detail', args=[issue.id])


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment_text = form.cleaned_data['text']
        updated_comment = form.instance
        updated_comment.date_edited = timezone.now()
        updated_comment.save()
        messages.success(
            self.request, f'The comment "{comment_text}" was updated successfully!')
        return super().form_valid(form)


@login_required
@test_issue_permissions
def set_milestone_view(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    project_milestones = Milestone.objects.filter(project=issue.project_id)
    return render(request, 'git/set_milestone.html', {'issue': issue, 'milestones': project_milestones})


@login_required
@test_issue_permissions
def set_milestone(request, issue_id, milestone_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    issue.milestone = milestone
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def clear_milestone(request, issue_id, milestone_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue.milestone = None
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def set_label_view(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    project_labels = Label.objects.filter(
        project=issue.project_id)
    applied_labels = issue.labels.all()
    applicable_labels = project_labels.exclude(
        id__in=[l.id for l in applied_labels])
    return render(request, 'git/apply_label.html', {'issue': issue, 'applicable_labels': applicable_labels})


@login_required
@test_issue_permissions
def apply_label(request, issue_id, label_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    label = get_object_or_404(Label, pk=label_id)
    issue.labels.add(label)
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def remove_label(request, issue_id, label_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue.labels.set(issue.labels.exclude(id=label_id))
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def set_assignees_view(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    project = Project.objects.filter(
        id=issue.project_id)
    project_collaborators = [* issue.project.collaborators.all(),
                             issue.author]
    existing_assignees = issue.assignees.all()
    available_assignees = [
        collaborator for collaborator in project_collaborators if collaborator not in existing_assignees]
    return render(request, 'git/assign_issue.html', {'issue': issue, 'available_assignees': available_assignees})


@login_required
@test_issue_permissions
def add_assignee(request, issue_id, assignee_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    assignee = get_object_or_404(User, pk=assignee_id)
    issue.assignees.add(assignee)
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def remove_assignee(request, issue_id, assignee_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue.assignees.set(issue.assignees.exclude(id=assignee_id))
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def close_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue.is_open = False
    issue.date_closed = timezone.now()
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_issue_permissions
def reopen_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue.is_open = True
    issue.save()
    return redirect(reverse('issue-detail', args=[issue_id]))


@login_required
@test_milestone_permissions
def close_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    milestone.is_open = False
    milestone.save()
    return redirect(reverse('project-detail', args=[milestone.project.id]))


@login_required
@test_milestone_permissions
def reopen_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    milestone.is_open = True
    milestone.save()
    return redirect(reverse('project-detail', args=[milestone.project.id]))
