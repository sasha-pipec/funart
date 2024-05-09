import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
app = Celery("conf")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_rating_themes": {
        "task": "api.tasks.theme.tasks.zeroing_rating_themes",
        "schedule": crontab(
            minute=0,
            hour=0,
        ),
    },
    'data_search': {
        'task': 'api.tasks.data_search.tasks.search_new_data',
        'schedule': crontab(
            minute=0,
            hour=0,
        ),
    }

}
