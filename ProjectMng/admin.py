from django.contrib import admin

# Register your models here.
from .models import Project, Issue, Task, Resource, DailyReport,Note

admin.site.register([Project, Issue, Task, Resource, DailyReport,Note])