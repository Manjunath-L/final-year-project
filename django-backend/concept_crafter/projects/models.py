from django.db import models
from django.conf import settings


class Project(models.Model):
    DIAGRAM_TYPES = [('mindmap', 'Mind Map'), ('flowchart', 'Flowchart')]

    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name         = models.CharField(max_length=255)
    project_type = models.CharField(max_length=20, choices=DIAGRAM_TYPES)
    data         = models.JSONField(default=dict)
    thumbnail    = models.TextField(blank=True, default='')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
