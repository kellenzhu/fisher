from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.view_models.trade import MyTrades
from app.models.base import db
from app.models.wish import Wish
from app.web import web


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    wish_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, wish_count_list)
    return render_template("my_wish.html", wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书已添加至您的赠送清单或心愿清单，请勿重复添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
