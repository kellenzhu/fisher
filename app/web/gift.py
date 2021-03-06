from flask import current_app
from flask_login import login_required, current_user

from app import web
from app.models.base import db
from app.models.gift import Gift


@web.route('/my/gifts')
@login_required
def my_gifts():
    return "My Gifts"


@web.route('/gifts/book/<isbn>')
def save_to_gifts(isbn):
    with db.auto_commit():
        gift = Gift()
        gift.isbn = isbn
        gift.uid = current_user.id
        current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
        db.session.add(gift)

    return


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
