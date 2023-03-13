"""Setup celery for the application."""

from celery import Celery

app = Celery(
    "celery_proj",
    broker="amqp://localhost",
    backend="redis://localhost:6379/0",
    include=["tasks"],
)


if __name__ == "__main__":
    app.start()
