"""Celery configuration and task definitions."""

from celery import Celery
from finsight.core.config import settings

# Initialize Celery app
celery_app = Celery(
    'finsight',
    broker=settings.redis_url,
    backend=settings.redis_url
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)
