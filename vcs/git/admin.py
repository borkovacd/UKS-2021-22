from django.contrib import admin
from .models import (
    Project,
    Issue,
    Milestone,
    Label
)

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Milestone)
admin.site.register(Label)
