"""
URL configuration for concept_crafter project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/generate/', include('ai_generator.urls')),
    path('api/templates/', include('templates_api.urls')),
]
