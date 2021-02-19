import json

from flask import jsonify, request

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
from app.web import web


@web.route('/book/search/')
def search():
    """
    http://127.0.0.1:5000/book/search/9787501524044/1
    http://127.0.0.1:5000/book/search?q=9787501524044&page=1
    http://127.0.0.1:5000/book/search?q=红楼梦
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == "isbn":
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)
        books.full(yushu_book, q)
        
        # TypeError: Object of type BookCollection is not JSON serializable
        # return jsonify(books)
        return json.dumps(books, default=lambda o: o.__dict__), 200, {"content-type": "application/json"}
    else:
        return jsonify(form.errors)
