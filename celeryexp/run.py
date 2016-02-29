"""
A simple test runner for comparing runtimes of two worker instances
started with possibly different options, both of which implement the
same two simple addition and multiplication tasks with a small sleep.

For instance:

shell1 $ celery worker -A celeryexp -n tasks1@leibniz -Q tasks1 -I celeryexp.tasks1 --loglevel=INFO -P prefork --concurrency 2 -Ofair
shell2 $ celery worker -A celeryexp -n tasks2@leibniz -Q tasks2 -I celeryexp.tasks2 --loglevel=INFO -P eventlet --concurrency 20 -Ofair
shell3 $ python -m celeryexp.run 100 100
"""
import sys
import time

from .tasks1 import add1
from .tasks2 import add2

add1_count, add2_count = int(sys.argv[1]), int(sys.argv[2])

add1_results = {}
add2_results = {}

running1 = running2 = 0

start = time.time()
while running1 < add1_count or running2 < add2_count:
    if running1 < add1_count:
        res = add1.delay(1001, running1)
        add1_results[res.task_id] = res
        running1 += 1
    if running2 < add2_count:
        res = add2.delay(2001, running2)
        add2_results[res.task_id] = res
        running2 += 1

runtime1 = runtime2 = None

while running1 or running2:
    if running1:
        for task_id, task in list(add1_results.items()):
            if task.state == 'SUCCESS':
                del add1_results[task_id]
                running1 -= 1
        if not running1:
            runtime1 = time.time() - start

    if running2:
        for task_id, task in list(add2_results.items()):
            if task.state == 'SUCCESS':
                del add2_results[task_id]
                running2 -= 1
        if not running2:
            runtime2 = time.time() - start

print('tasks1 runtime: %s' % runtime1)
print('tasks2 runtime: %s' % runtime2)
