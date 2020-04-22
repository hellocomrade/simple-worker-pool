import sys
import time

from multiprocessing import Process, Queue, Pool, Manager


def worker(idx, queue):
    print(f'Worker {idx} is up')
    while True:
        msg = queue.get()
        print(f'Worker {idx}: {msg}')
        time.sleep(1)


if '__main__' == __name__:
    cores = max(1, 2 if 1 == len(sys.argv) else int(sys.argv[1]))
    mgr = Manager()
    q = mgr.Queue()
    pool = Pool(cores)
    workers = [pool.apply_async(worker, (i, q)) for i in range(cores)]
    for i in range(20):
        q.put(2**i)
    try:
        [worker.get() for worker in workers]
    except:
        pool.terminate()
        pool.join()