from django.urls import path
from .views import GenerateView

urlpatterns = [
    path('', GenerateView.as_view(), name='generate'),
]
