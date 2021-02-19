class MyResource:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_value:
            print(exc_value)

    def query(self):
        print("Query resource")


with MyResource() as mr:
    1 / 0
    mr.query()
