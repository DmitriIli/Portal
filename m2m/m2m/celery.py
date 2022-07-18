import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm2m.settings')

app = Celery('m2m')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_second': {
        'task': 'news.tasks.weekly_notify',  # задача
        'schedule': crontab(minute='0', hour='8', day_of_week='1'),
        'args': ()
    },
}
