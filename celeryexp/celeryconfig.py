from kombu import Exchange, Queue

BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True,
    'fanout_patterns': True,
    # visibility timeout should be at least as long as the longest
    # ETA that will be used; if not acknowledged before timeout,
    # it will be redelivered to another worker and executed.
    'visibility_timeout': 3600,
}


CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CELERY_DISABLE_RATE_LIMITS = True
# CELERY_ACKS_LATE = True
# CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ACKS_LATE = False

# serialize using json (consider yaml if dates needed later);
# see http://docs.kombu.me/en/latest/userguide/serialization.html
# for how to define custom serializers (would be nice to have one that
# supported datetimes and was secured via a strong MAC)
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# Couldn't get routing working using autoconfigure
CELERY_QUEUES = (
    Queue('tasks1', exchange=Exchange('tasks1'), routing_key='tasks1'),
    Queue('tasks2', exchange=Exchange('tasks2'), routing_key='tasks2'),
)


class Router:

    def route_for_task(self, task, args=None, kwargs=None):
        # task will be something like 'celeryexp.tasks1.add1'
        names = task.split('.')
        if len(names) > 2 and names[0] == 'celeryexp':
            return {
                'exchange': names[1],
                'routing_key': names[1],
            }

CELERY_ROUTES = (Router(), )
