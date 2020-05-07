import sys
import json
import pika


def callback(ch, method, properties, body):
    print(len(body))


def main(message_queue_host, message_queue_exchange, message_queue_name):
    def get_channel():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=message_queue_host, heartbeat=600, blocked_connection_timeout=300))
        channel = connection.channel()
        channel.queue_bind(exchange=message_queue_exchange, queue=message_queue_name)
        channel.basic_consume(queue=message_queue_name, on_message_callback=callback, auto_ack=True)
        return channel

    print('Start consuming...')
    channel = get_channel()
    while True:
        try:
            channel.start_consuming()
        except pika.exceptions.StreamLostError as e:
            channel = get_channel()


if '__main__' == __name__:
    if 4 > len(sys.argv):
        print(f'{__file__} message_queue_host, message_queue_exchange_name, message_queue_name')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])