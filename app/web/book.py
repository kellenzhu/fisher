from flask import request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
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
        # return json.dumps(books, default=lambda o: o.__dict__), 200, {"content-type": "application/json"}
    else:
        # return jsonify(form.errors)
        flash(message="搜索的关键字不符合要求，请重新输入关键字")
    return render_template("search_result.html", books=books)


@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    # 图书detail页面
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 页面展示wish和gift
    has_in_gift = False
    has_in_wish = False
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gift = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wish = True
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts_models = TradeInfo(trade_gifts)
    trade_wishes_models = TradeInfo(trade_wishes)
    return render_template("book_detail.html", book=book, wishes=trade_wishes_models, gifts=trade_gifts_models,
                           has_in_gifts=has_in_gift, has_in_wishes=has_in_wish)
