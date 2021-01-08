from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','simplifyML.settings')

app = Celery('simplifyML')
app.conf.update(
    BROKER_URL = 'redis://@127.0.0.1:6379/4'
)

app.autodiscover_tasks(settings.INSTALLED_APPS)