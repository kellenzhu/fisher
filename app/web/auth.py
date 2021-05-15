from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user

from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from app.web import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for("web.index"))
    return render_template("auth/register.html", form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            jump_page = request.args.get("next")
            if not jump_page or not jump_page.startswith("/"):
                return redirect(url_for("web.index"))
            return redirect(jump_page)
        else:
            flash(message="用户不存在，请重新输入")
    return render_template("auth/login.html", form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("web.index"))
