from django.urls import path
from .views.auth_views import RegisterView, LoginView, MeView
from .views.project_views import ProjectListView, ProjectDetailView
from .views.template_views import TemplateListView, TemplateDetailView
from .views.generate_views import GenerateView

urlpatterns = [
    # Auth
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/me', MeView.as_view()),

    # Projects
    path('projects', ProjectListView.as_view()),
    path('projects/<int:pk>', ProjectDetailView.as_view()),

    # Templates
    path('templates', TemplateListView.as_view()),
    path('templates/<int:pk>', TemplateDetailView.as_view()),

    # AI Generate
    path('generate', GenerateView.as_view()),
]
