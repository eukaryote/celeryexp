from . import celery
from .util import dump, pause


@celery.task
def add1(x, y):
    pause()
    return dump('/tmp/tasks1.add1', x + y)


@celery.task
def multiply1(x, y):
    pause()
    return dump('/tmp/tasks1.multiply1', x * y)
