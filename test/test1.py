import threading
import time


def worker():
    print("I'm worker")
    t = threading.currentThread()
    time.sleep(10)
    print("this worker def", t.getName())


# new_t = threading.Thread(target=worker, name="2nd_Threading")
# new_t.start()
worker()

print("I'm main threading")
print(threading.currentThread().getName())
