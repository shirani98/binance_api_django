from datetime import datetime, timedelta
from celery import shared_task
from data.models import Data, Result


@shared_task
def calculate_result():
    data = Data.objects.filter(status=True)
    for item in data :
        Result.get_result(item.uuid)

@shared_task
def delete_older_result():
    time = datetime.now() - timedelta(minutes= 1)
    result = Result.objects.filter(created__lte = time)
    result.delete()

