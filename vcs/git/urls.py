from django.urls import path

from git.models import Label
from . import views
from .views import (
    CommentDeleteView,
    CommentUpdateView,
    IssueDetailView,
    IssueDeleteView,
    LabelCreateView,
    LabelUpdateView,
    LabelDeleteView,
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='git-home'),

    path('projects/', views.projects, name='projects'),
    path('new-project/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/',
         ProjectDeleteView.as_view(), name='project-delete'),

    path('new-collaborator/<int:project_id>/',
         views.add_collaborator, name='new-collaborator'),
    path('project/<int:project_id>/collaborators/<int:collaborator_id>/delete/',
         views.delete_collaborator, name='collaborator-delete'),

    path('milestones/<int:project_id>', views.milestones, name='milestones'),
    path('milestone-form/<int:project_id>',
         views.milestone_form, name='milestone-form'),
    path('new-milestone/<int:project_id>',
         views.new_milestone, name='new-milestone'),
    path('delete-milestone/<int:milestone_id>/<int:project_id>',
         views.delete_milestone, name='delete-milestone'),

    path('project/<int:project_id>/new-label/',
         LabelCreateView.as_view(), name='label-create'),
    path('label/<int:pk>/update/', LabelUpdateView.as_view(), name='label-update'),
    path('label/<int:pk>/delete/', LabelDeleteView.as_view(), name='label-delete'),

    path('project/<int:project_id>/new-issue/',
         views.add_issue, name='issue-create'),
    path('issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('issues/<int:pk>/delete/',
         IssueDeleteView.as_view(), name='issue-delete'),
    path('issues/<int:issue_id>/set-milestone/',
         views.set_milestone_view, name='set-milestone-view'),
    path('issues/<int:issue_id>/set-milestone/<int:milestone_id>/set/',
         views.set_milestone, name='set-milestone'),
    path('issues/<int:issue_id>/set-milestone/<int:milestone_id>/clear/',
         views.clear_milestone, name='clear-milestone'),
    path('issues/<int:issue_id>/set-label/',
         views.set_label_view, name='set-label-view'),
    path('issues/<int:issue_id>/set-label/<int:label_id>/apply/',
         views.apply_label, name='apply-label'),
    path('issues/<int:issue_id>/set-label/<int:label_id>/remove/',
         views.remove_label, name='remove-label'),
    path('issues/<int:issue_id>/set-assignees/',
         views.set_assignees_view, name='set-assignees-view'),
    path('issues/<int:issue_id>/add-assignee/<int:assignee_id>/add/',
         views.add_assignee, name='add-assignee'),
    path('issues/<int:issue_id>/remove-assignee/<int:assignee_id>/remove/',
         views.remove_assignee, name='remove-assignee'),


    path('comment/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:pk>/update/',
         CommentUpdateView.as_view(), name='comment-update'),




]
