import celery_conf


@celery_conf.app.task
def add(x: int, y: int) -> int:
    """Return sum of two numbers."""
    return x + y
