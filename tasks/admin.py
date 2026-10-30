from django.contrib import admin
from taskflow.tasks.models import Task


admin.site.register(Task)
