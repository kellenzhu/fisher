from flask import current_app, redirect, url_for, flash, render_template
from flask_login import login_required, current_user

from app.view_models.trade import MyTrades
from app.web import web
from app.models.base import db
from app.models.gift import Gift


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template("my_gifts.html", gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            db.session.add(gift)
    else:
        flash("这本书已经存在于心愿清单，请勿重复添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
