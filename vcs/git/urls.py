from django.urls import path
from . import views
from .views import (
    ProjectListView,
    ProjectDetailView
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='git-home'),

    path('projects/', views.projects, name='projects'),
    path('project-form/', views.project_form, name='project-form'),
    path('new-project/', views.new_project, name='new-project'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),

    path('milestones/<int:project_id>', views.milestones, name='milestones'),
    path('milestone-form/<int:project_id>',
         views.milestone_form, name='milestone-form'),
    path('new-milestone/<int:project_id>',
         views.new_milestone, name='new-milestone'),
    path('delete-milestone/<int:milestone_id>/<int:project_id>',
         views.delete_milestone, name='delete-milestone')
]
