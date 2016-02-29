import time
import random


def dump(path, value):
    "Append value (converting to str and appending newline) to file at path."
    msg = (str(value) + '\n').encode('utf8')
    with open(path, 'ab') as f:
        f .write(msg)
    return value


def pause(seconds=0.1):
    time.sleep(random.random() * seconds)
