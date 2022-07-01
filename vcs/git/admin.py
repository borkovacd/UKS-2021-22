from django.contrib import admin
from .models import (
    Project,
    Milestone,
    Label
)

admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(Label)
