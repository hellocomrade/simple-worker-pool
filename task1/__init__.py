import pika

from celery import Celery
from celery import signals

from task1 import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)


@signals.worker_process_init.connect
def init_worker(sender, signal, **kwargs):
    global connection
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=celeryconfig.message_queue_host))
    channel = connection.channel()
    print(channel)


@signals.worker_process_shutdown.connect
def shutdown_worker(sender, **kwargs):
    global connection
    if connection:
        connection.close()