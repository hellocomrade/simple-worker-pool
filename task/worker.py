import json

from . import app
from . import socket_lst


@app.task(bind=True, ignore_result=True)
def send(self, msg):
    obj = json.loads(msg)
    if 'wav' in obj:
        for wav in obj['wav']:
            if '1814' == wav['id']:
                for sck in socket_lst:
                    sck.send(msg.encode())