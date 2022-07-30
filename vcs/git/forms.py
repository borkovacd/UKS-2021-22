from django import forms
from .models import (
    Issue,
    Project,
    Label,
    Comment
)
from django.contrib.auth.models import User
from django.db.models import Q


class CollaboratorsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['collaborators']
        IsCollaborationPossible = True

    def __init__(self, currentUserId, existingCollaborators, *args, **kwargs):
        super(CollaboratorsForm, self).__init__(*args, **kwargs)
        CollaboratorsForm.__filterCollaboratorList(
            self, currentUserId, existingCollaborators)
        CollaboratorsForm.__setIsCollaborationPossibleFlag(self)

    def __filterCollaboratorList(self, currentUserId, existingCollaborators):
        self.fields['collaborators'].queryset = User.objects.filter(is_superuser=False).filter(
            ~Q(id=currentUserId)).exclude(id__in=[c.id for c in existingCollaborators])

    def __setIsCollaborationPossibleFlag(self):
        if not self.fields['collaborators'].queryset:
            self.IsCollaborationPossible = False


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['title', 'color', 'description']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'milestone', 'labels', 'assignees']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
