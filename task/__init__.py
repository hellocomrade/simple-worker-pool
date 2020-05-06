import socket

from celery import Celery
from celery import signals

from task import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)

socket_lst = list()


# https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script
def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


@signals.worker_process_init.connect
def init_worker(sender, signal, **kwargs):
    for li in celeryconfig.listener_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((li['host'], li['port']))
        set_keepalive_linux(sock)
        socket_lst.append(sock)
        # print(f'socket: {len(socket_lst)}')


@signals.worker_process_shutdown.connect
def shutdown_worker(sender, **kwargs):
    for sock in socket_lst:
        sock.close()