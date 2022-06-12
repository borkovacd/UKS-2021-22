from django.contrib import admin
from .models import (
    Project,
    Milestone
)

admin.site.register(Project)
admin.site.register(Milestone)