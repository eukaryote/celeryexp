from celery import Celery

celery = Celery('myapp')
celery.config_from_object('celeryexp.celeryconfig')
