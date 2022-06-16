from django.urls import path
from . import views
from .views import (
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateView
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='git-home'),

    path('projects/', views.projects, name='projects'),
    path('new-project/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(), name='project-update'),

    path('milestones/<int:project_id>', views.milestones, name='milestones'),
    path('milestone-form/<int:project_id>',
         views.milestone_form, name='milestone-form'),
    path('new-milestone/<int:project_id>',
         views.new_milestone, name='new-milestone'),
    path('delete-milestone/<int:milestone_id>/<int:project_id>',
         views.delete_milestone, name='delete-milestone')
]
