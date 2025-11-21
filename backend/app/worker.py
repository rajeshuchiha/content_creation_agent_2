from app.celery_app import celery
from app import tasks  # Register tasks

# This file is just to ensure tasks are imported when worker starts