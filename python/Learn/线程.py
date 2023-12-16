import os
from threading import Thread
import time
import random

def bg_thread():
    for i in range(1, 30):
        print(f'{i} of 30 iterations...')
        time.sleep(random.random())  # do some work...

    print(f'{i} iterations completed before exiting.')

th = Thread(target=bg_thread)
th.setDaemon(True)
th.start()
th.join()