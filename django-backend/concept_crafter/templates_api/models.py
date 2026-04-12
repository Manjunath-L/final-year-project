from django.db import models


class Template(models.Model):
    DIAGRAM_TYPES = [('mindmap', 'Mind Map'), ('flowchart', 'Flowchart')]

    name        = models.CharField(max_length=255)
    type        = models.CharField(max_length=20, choices=DIAGRAM_TYPES)
    data        = models.JSONField(default=dict)
    thumbnail   = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name
