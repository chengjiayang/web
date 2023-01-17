from __future__ import absolute_import, unicode_literals

import logging
import os
from celery import Celery, platforms
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')


app = Celery('myweb', backend='redis://127.0.0.1:6379/1', broker='redis://127.0.0.1:6379/2')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    logging.info('Request: {0!r}'.format(self.request))
    logging.info("执行celery.py:debug_task")