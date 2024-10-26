from django.db import models
from django.contrib.auth.models import User
# from telegram_django_bot.models import TelegramUser


# class User(TelegramUser):
#     pass

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    ISSUE_TYPES = (
        ('APP', 'App'),
        ('DB', 'Database'),
        ('CONFIG', 'Configuration'),
        ('PROBLEM', 'Problem Solved'),
        ('INSTALL', 'Installation'),
        ('OTHER', 'Other'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=100)
    description = models.TextField()
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.title}"

class Task(models.Model):
    STATUS_CHOICES = (
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUSPENDED','Suspended'),
        ('DONE', 'Done'),
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.issue.project.name} - {self.title}"

class Note(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.issue.title}"

class Resource(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_reports')
    date = models.DateField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Daily Report - {self.user.username} - {self.date}"