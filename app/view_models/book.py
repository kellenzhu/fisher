class BookViewModel:
    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.pages = book["pages"]
        self.author = "、".join(book["author"])
        self.price = book["price"]
        self.summary = book["summary"] or ""
        self.image = book["image"]
        self.isbn = book["isbn"]

    @property
    def intro(self):
        """
        图书基本信息显示
        :return: author/publisher/price
        """
        # intros = []
        # if self.author:
        #     intros.append(self.author)
        # if self.publisher:
        #     intros.append(self.publisher)
        # if self.price:
        #     intros.append(self.price)
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])

        return "/".join(intros)


class BookCollection:
    def __init__(self):
        self.books = []
        self.total = 0
        self.keyword = ""

    def full(self, yushu_book, keyword):
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.total = yushu_book.total
        self.keyword = keyword


class _BookViewModel:

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned["total"] = 1
            returned["books"] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned["total"] = data["total"]
            returned["books"] = [cls.__cut_book_data(book) for book in data["books"]]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"] or "",
            "author": "、".join(data["author"]),
            "price": data["price"],
            "summary": data["summary"] or "",
            "image": data["image"]
        }

        return book
