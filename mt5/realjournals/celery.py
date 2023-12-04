from __future__ import absolute_import, unicode_literals
import random
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realjournals.settings")

from django.conf import settings

app = Celery('realjournals')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
