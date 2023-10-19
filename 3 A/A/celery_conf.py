from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')

celery_app = Celery('A')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.update(
    task_serializer='json',
    result_serializer='pickle',
    accept_content=['json', 'pickle'],
    result_expires=timedelta(days=1),
    task_always_eager=False,
    worker_prefetch_multiplier=4,
)
