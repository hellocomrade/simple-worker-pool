import pika

from celery import Celery
from celery import signals

from task1 import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)

connection = None
# Global variable remains None after init_worker is called. Probably because import is completed before init_worker
# is called? using a list will solve this for now...
channel = list()


@signals.worker_process_init.connect
def init_worker(sender, signal, **kwargs):
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=celeryconfig.message_queue_host))
    channel.append(connection.channel())


@signals.worker_process_shutdown.connect
def shutdown_worker(sender, **kwargs):
    global connection
    if connection:
        connection.close()