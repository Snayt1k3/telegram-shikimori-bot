from celery import Celery
from src.config.redis import redis_cfg

celery_app = Celery("anime_service", broker=redis_cfg.url, backend=redis_cfg.url)

celery_app.conf.update(
    task_routes={"tasks.*": {"queue": "anime_queue"}}, task_serializer="json"
)
