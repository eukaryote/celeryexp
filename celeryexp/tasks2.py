from . import celery
from .util import dump, pause


@celery.task
def add2(x, y):
    pause()
    return dump('/tmp/tasks2.add2', x + y)


@celery.task
def multiply2(x, y):
    pause()
    return dump('/tmp/tasks2.multiply2', x * y)
