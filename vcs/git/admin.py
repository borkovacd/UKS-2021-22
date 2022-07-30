from django.contrib import admin
from .models import (
    Project,
    Issue,
    Milestone,
    Label,
    Comment
)

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Milestone)
admin.site.register(Label)
admin.site.register(Comment)
