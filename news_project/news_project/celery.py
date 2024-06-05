import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')


app = Celery('news_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'refresh-search-results-every-hour': {
        'task': 'news.tasks.refresh_search_results',
        'schedule': crontab(minute=0, hour='*/1'),  # Every hour
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')