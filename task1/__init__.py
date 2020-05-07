import pika

from celery import Celery
from celery import signals

from task import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)

connection = None
channel = None


@signals.worker_process_init.connect
def init_worker(sender, signal, **kwargs):
    global  connection
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=celeryconfig.message_queue_host))
    channel = connection.channel()


@signals.worker_process_shutdown.connect
def shutdown_worker(sender, **kwargs):
    connection.close()