from django.urls import path

from git.models import Label
from . import views
from .views import (
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
    path('label/<int:pk>/delete/', LabelDeleteView.as_view(), name='label-delete')

]
