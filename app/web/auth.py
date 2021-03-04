from flask import render_template, request

from app.forms.auth import RegisterForm
from app.models.user import User
from app.web import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        user = User()
        user.email = form.email.data()

    return render_template("auth/register.html", form={"data": {}})

@web.route('/login', methods=['GET', 'POST'])
def login():
    pass


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
    pass
