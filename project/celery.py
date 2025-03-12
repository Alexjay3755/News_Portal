import os
from celery import Celery
from celery.schedules import crontab
from celery.schedules import solar

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'simpleapp.tasks.my_job',
        'schedule': crontab(hour='12', minute='00', day_of_week='wednesday'),
    },
}


