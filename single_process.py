import sys
import json
import pika

if '__main__' == __name__:
    if 4 > len(sys.argv):
        print(f'{__file__} message_queue_host, message_queue_exchange_name, data_file_path', file=sys.stderr)
    mq_host, mq_exchange, path = str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
    channel = connection.channel()
    with open(path, 'r') as f:
        for line in f:
            obj = json.loads(line)
            if 'wav' in obj:
                for wav in obj['wav']:
                    if '1814' == wav['id']:
                        channel.basic_publish(exchange=mq_exchange, routing_key='shock-index', body=line)
                        break