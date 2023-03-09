"""Setup celery for the application."""

from celery import Celery

app = Celery(
    "celery_proj",
    broker="amqp://localhost",
    backend="rpc://",
    include=["tasks"],
)


if __name__ == "__main__":
    app.start()
