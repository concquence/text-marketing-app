import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'text_marketing.settings')

app = Celery('text_marketing')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
