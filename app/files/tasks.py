from celery import shared_task

from files.models import File


@shared_task
def process_uploaded_file(file_id):
    """ Celery task to process uploaded file """
    try:
        file_instance = File.objects.get(id=file_id)
        file_instance.processed = True
        file_instance.save()
    except File.DoesNotExist:
        pass
