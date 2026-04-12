from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    # Expose 'type' in JSON, mapping to/from 'project_type' on the model
    type = serializers.CharField(source='project_type')

    class Meta:
        model = Project
        fields = ('id', 'type', 'name', 'data', 'thumbnail', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
