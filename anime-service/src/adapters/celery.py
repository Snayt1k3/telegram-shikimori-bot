from celery import Celery
from src.config.redis import redis_cfg

celery_app = Celery("anime_service", broker=redis_cfg.url, backend=redis_cfg.url)

celery_app.conf.update(
    task_routes={"tasks.*": {"queue": "anime_queue"}},
    task_serializer="json",
    accept_content=["json"],
    result_expires=3600,
    worker_log_level="INFO",
    worker_log_format="[%(asctime)s: %(levelname)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s] %(task_name)s: %(message)s",
)

if __name__ == "__main__":
    celery_app.start()
