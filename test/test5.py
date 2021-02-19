# LocalStack Test file
import threading
import time

from werkzeug.local import LocalStack

ls = LocalStack()
# 主线程中对ls栈中推入元素
ls.push(1)


def worker():
    # 新的线程中，将会创建一个新栈与主线程隔离互不影响，这里刚创建的栈所以为空
    print("新线程中取栈顶元素", ls.top)
    ls.push(2)
    print("推入元素后在查看栈顶元素", ls.top)


new_thread = threading.Thread(target=worker, name="newThread")
new_thread.start()
time.sleep(1)
print("此时主线程中栈顶元素", ls.top)
