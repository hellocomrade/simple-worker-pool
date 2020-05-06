import sys
import json
import pika


def callback(ch, method, properties, body):
    print(body)


def main(message_queue_host, message_queue_exchange, message_queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=message_queue_host))
    channel = connection.channel()
    channel.queue_bind(exchange=message_queue_exchange, queue=message_queue_name)
    channel.basic_consume(queue=message_queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if '__main__' == __name__:
    if 4 > len(sys.argv):
        print(f'{__file__} message_queue_host, message_queue_exchange_name, message_queue_name')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])