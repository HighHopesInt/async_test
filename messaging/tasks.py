"""Tasks description module."""
from celery import Celery

import random
import docker

from celery import Celery

APP = Celery('tasks', backend='rpc://', broker='amqp://', include=['messaging.tasks'])

# CLIENT = docker.APIClient(base_url='unix://var/run/docker.sock')

@APP.task
def build_image(**kwargs):
    """Builds docker image with specified parameters."""
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    if kwargs["tag_image"] == "default":
        kwargs["tag_image"] = "default{}".format(random.randint(1, 100000))

    url = "{}.git".format(kwargs["url_address"])

    # output = [line for line in CLIENT.build(path=url, rm=True, tag=kwargs["tag_image"])]

    lines = []

    for line in client.build(path=url, rm=True, tag=kwargs["tag_image"]):
        lines.append(line)
        build_image.update_state(state='PROGRESS', meta={'line': lines})
    # return 0


@APP.task(ignore_result=True)
def print_hello():
    """Test task."""
    print('hello there')


@APP.task
def gen_prime(value):
    """Long lasting test task."""
    multiples = []
    results = []
    for i in range(2, value+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, value+1, i):
                multiples.append(j)
    return results
