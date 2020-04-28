import sys
import json
import pika

from multiprocessing import Process, Queue, Pool, Manager


def worker(idx, queue, message_queue_host, message_queue_exchange):
    print(f'Worker {idx} is up')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=message_queue_host))
    channel = connection.channel()
    while True:
        msg = queue.get()
        # print(f'Worker {idx}: {msg}')
        obj = json.loads(msg)
        if 'wav' in obj:
            for wav in obj['wav']:
                if '1814' == wav['id']:
                    channel.basic_publish(exchange=message_queue_exchange, routing_key='shock-index', body=msg)
                    break
    # connection.close()


def listener(dpath, q):
    with open(dpath, 'r') as f:
        for line in f:
            q.put(line)


if '__main__' == __name__:
    if 5 > len(sys.argv):
        print(f'{__file__} number_of_worker, message_queue_host, message_queue_exchange_name, data_file_path', file=sys.stderr)
        sys.exit()
    cores, mq_host, mq_exchange, path = max(1, int(sys.argv[1])), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4])
    mgr = Manager()
    q = mgr.Queue()
    pool = Pool(cores)
    workers = [pool.apply_async(worker, (i, q, mq_host, mq_exchange)) for i in range(cores)]
    Process(target=listener, args=(path, q)).start()

    try:
        [worker.get() for worker in workers]
    except Exception as e:
        pool.terminate()
        pool.join()