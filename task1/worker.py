import json

from . import app, channel
from . import celeryconfig


@app.task(bind=True, ignore_result=True)
def send(self, msg):
    obj = json.loads(msg)
    if 'wav' in obj:
        for wav in obj['wav']:
            if '1814' == wav['id']:
                channel.basic_publish(exchange=celeryconfig.message_queue_exchange, routing_key=celeryconfig.message_queue_routing_key, body=msg)
                break
