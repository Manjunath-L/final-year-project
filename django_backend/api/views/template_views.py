from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Template
from ..serializers import TemplateSerializer


class TemplateListView(APIView):
    def get(self, request):
        templates = Template.objects.all()
        return Response(TemplateSerializer(templates, many=True).data)


class TemplateDetailView(APIView):
    def get(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({'message': 'Template not found'}, status=404)
        return Response(TemplateSerializer(template).data)
