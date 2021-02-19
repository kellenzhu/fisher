import threading
import time

from werkzeug.local import Local

my_obj = Local()
my_obj.a = 1


def worker():
    my_obj.a = 2
    print("new thread a is ", my_obj.a)


new_thread = threading.Thread(target=worker, name="new_thread")
new_thread.start()
time.sleep(2)

print("main thread a is", my_obj.a)
