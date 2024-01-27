import os
from celery import Celery
from celery.schedules import crontab

import redis

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_posts_notification': {
        'task': 'news.tasks.week_news_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

# red = redis.Redis(
#     host='redis-17393.c228.us-central1-1.gce.cloud.redislabs.com',
#     port=17393,
#     password='Vet7nJ0FXRSmQBLTqvRmYlEw9pYjbES3'
# )