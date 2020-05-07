import json

from . import app
from . import celeryconfig


@app.task(bind=True, ignore_result=True)
def send(self, msg):
    from . import channel
    obj = json.loads(msg)
    if 'wav' in obj:
        for wav in obj['wav']:
            if '1814' == wav['id']:
                channel[0].basic_publish(exchange=celeryconfig.message_queue_exchange, routing_key=celeryconfig.message_queue_routing_key, body=msg)
                break
