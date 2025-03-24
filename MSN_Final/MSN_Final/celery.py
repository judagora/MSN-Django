from celery import Celery
import os
import billiard as multiprocessing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSN_Final.settings')
app = Celery('MSN_Final')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()