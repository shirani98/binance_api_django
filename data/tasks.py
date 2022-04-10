from celery import shared_task
from data.models import ArchiveData, Data
from datetime import datetime, timedelta


@shared_task
def calculate_result():
    data = Data.objects.filter(status=True)
    for item in data :
        Data.get_result(item.uuid)
        
@shared_task
def clean_archive():
    time = datetime.now() - timedelta(minutes=1)
    data = ArchiveData.objects.filter(created__lt = time )
    data.delete()



