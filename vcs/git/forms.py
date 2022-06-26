from django import forms
from .models import (
    Project
)
from django.contrib.auth.models import User
from django.db.models import Q


class CollaboratorsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['collaborators']

    def __init__(self, currentUserId, existingCollaborators, *args, **kwargs):
        super(CollaboratorsForm, self).__init__(*args, **kwargs)
        CollaboratorsForm.__excludeCurrentUserAndSuperUsers(
            self, currentUserId, existingCollaborators)

    def __excludeCurrentUserAndSuperUsers(self, currentUserId, existingCollaborators):
        self.fields['collaborators'].queryset = User.objects.filter(is_superuser=False).filter(
            ~Q(id=currentUserId)).exclude(id__in=[c.id for c in existingCollaborators])
