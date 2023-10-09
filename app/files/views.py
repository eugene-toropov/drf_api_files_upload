from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from files.models import File
from files.serializers import FileSerializer
from files_api.celery import app as celery_app


class FileCreateView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            file_instance = File.objects.create(file=request.FILES['file'])
            celery_app.send_task('files.tasks.process_uploaded_file', args=[file_instance.id])
            serializer = FileSerializer(file_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error')
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FileListView(ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
