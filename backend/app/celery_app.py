from celery import Celery
import os
from app.logger import setup_logger

logger = setup_logger(__name__)

# Explicitly set Redis URLs
broker_url = os.getenv('CELERY_BROKER', 'redis://redis:6379/0')
result_backend = os.getenv('CELERY_BACKEND', 'redis://redis:6379/1')

# Create Celery instance with explicit broker
celery = Celery(
    'worker',
    broker=broker_url,
    backend=result_backend
)

# IMPORTANT: Explicitly update configuration to ensure Redis is used
celery.conf.update(
    broker_url=broker_url,  # Explicitly set again
    result_backend=result_backend,  # Explicitly set again
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

# celery.set_default()
# print(f"[CELERY INIT] Celery app set as default")
# print(f"[CELERY INIT] Final broker: {celery.conf.broker_url}")

# # Autodiscover tasks
# # celery.autodiscover_tasks(['app.tasks'])

# # NOW import tasks (this ensures they use the configured app)
from app import tasks  # This will trigger task registration

logger.info(f"[CELERY INIT] Tasks imported")