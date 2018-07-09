from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anf_man.settings')

app = Celery('anf_man')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-every-seconds': {
        'task': 'tr_helper.tasks.check_if_new',
        'schedule': 1.0,
    },
}
