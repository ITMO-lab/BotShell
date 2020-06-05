# -*- coding: utf8 -*-

from main.core.db.synchronized.local.local_shared_data import LocalSharedData
import threading
import time

threads = []

if __name__ == '__main__':
    threads.append(threading.Thread(target=LocalSharedData.set, args=(22222, 123, ('my', 'little', 'pony', ))))
    threads.append(threading.Thread(target=LocalSharedData.set, args=(22222, 1234, ('my', 'little', 'pony', ))))
    threads.append(threading.Thread(target=LocalSharedData.get, args=(22222, )))
    threads.append(threading.Thread(target=LocalSharedData.set, args=(22222, 'test', ('data', ))))
    threads.append(threading.Thread(target=LocalSharedData.get, args=(22222, )))
    threads.append(threading.Thread(target=LocalSharedData.remove, args=(22222, ('mssy', ))))
    threads.append(threading.Thread(target=LocalSharedData.get, args=(22222, )))
    threads.append(threading.Thread(target=LocalSharedData.remove, args=(22222, ('my', 'little', 'pony'))))
    threads.append(threading.Thread(target=LocalSharedData.get, args=(22222, )))
    threads.append(threading.Thread(target=LocalSharedData.set, args=(22222, 'test', ('my', 'little', ))))
    threads.append(threading.Thread(target=LocalSharedData.get, args=(22222, )))
    threads.append(threading.Thread(target=LocalSharedData.remove, args=(22222, )))
    threads.append(threading.Thread(target=LocalSharedData.get, args=(22222, )))

    for thread in threads:
        thread.start()
