from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Template
from .serializers import TemplateSerializer


class TemplateListView(ListAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [AllowAny]
