import sys
import pika
import socketserver


class PacketHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print(f'Handling incoming traffic from {self.client_address[0]}:{self.client_address[1]}')

        def get_channel():
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, heartbeat=600, blocked_connection_timeout=300))
            return connection.channel()
        channel = get_channel()
        msg = None
        while True:
            try:
                if not msg:
                    msg = self.rfile.readline().rstrip().decode()
                channel.basic_publish(exchange=mq_exchange, routing_key='shock-index', body=msg)
                msg = None
            except pika.exceptions.StreamLostError as e:
                channel = get_channel()


if '__main__' == __name__:
    if 5 != len(sys.argv):
        print(f'{__file__} listener_host port message_queue_host, message_queue_exchange_name')
    else:
        mq_host, mq_exchange = str(sys.argv[3]), str(sys.argv[4])
        listener = socketserver.ForkingTCPServer((sys.argv[1], int(sys.argv[2])), PacketHandler)
        try:
            listener.serve_forever()
        except Exception as e:
            print(str(e), file=sys.stderr)