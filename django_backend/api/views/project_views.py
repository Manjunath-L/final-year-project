from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Project
from ..serializers import ProjectSerializer


class ProjectListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('userId')
        qs = Project.objects.all()
        if user_id:
            qs = qs.filter(user_id=user_id)
        return Response(ProjectSerializer(qs, many=True).data)

    def post(self, request):
        data = request.data.copy()
        if 'data' not in data:
            data['data'] = {}

        # Map userId -> user_id for the serializer
        if 'userId' in data:
            data['user_id'] = data.pop('userId')

        project = Project.objects.create(
            name=data.get('name'),
            type=data.get('type'),
            data=data.get('data', {}),
            thumbnail=data.get('thumbnail', ''),
            user_id=data.get('user_id'),
        )
        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)


class ProjectDetailView(APIView):
    def _get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        project = self._get_project(pk)
        if not project:
            return Response({'message': 'Project not found'}, status=404)
        return Response(ProjectSerializer(project).data)

    def put(self, request, pk):
        project = self._get_project(pk)
        if not project:
            return Response({'message': 'Project not found'}, status=404)

        update = request.data
        if 'name' in update:
            project.name = update['name']
        if 'type' in update:
            project.type = update['type']
        if 'data' in update:
            project.data = update['data']
        if 'thumbnail' in update:
            project.thumbnail = update['thumbnail']
        project.save()
        return Response(ProjectSerializer(project).data)

    def delete(self, request, pk):
        project = self._get_project(pk)
        if not project:
            return Response({'message': 'Project not found'}, status=404)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
