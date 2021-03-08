class MyResource:
    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, exc_type, exc_value, tb):
    #     if exc_value:
    #         print(exc_value)

    def query(self):
        print("Query resource")


# with MyResource() as mr:
#     mr.query()

from contextlib import contextmanager


@contextmanager
def test():
    print("Connect")
    yield MyResource()
    print("Stop")


with test() as t:
    t.query()
