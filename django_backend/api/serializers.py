from rest_framework import serializers
from .models import User, Project, Template


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id', required=False, allow_null=True)

    class Meta:
        model = Project
        fields = ['id', 'userId', 'name', 'type', 'data', 'thumbnail', 'created_at', 'updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['createdAt'] = rep.pop('created_at')
        rep['updatedAt'] = rep.pop('updated_at')
        return rep


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', 'type', 'data', 'thumbnail', 'description']
