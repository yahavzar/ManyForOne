from flask import Blueprint, render_template, request, redirect, session
from DB import get_user
from datetime import datetime

login_page = Blueprint('Login', __name__, template_folder='../templates')


@login_page.route('/Login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get("Email")
        password = request.form.get("Password")
        loginFlag = check_login(email, password)
        # If user doesn't exist in database, redirect to register page
        if loginFlag == -1:
            return redirect("/Register")
        else:
            if loginFlag == 0:
                return render_template("LoginPage.html", loginFlag="0")

        # Login data is correct
        set_session_data(email.lower(), password)
        return redirect("/")
    return render_template("LoginPage.html")


# Checks login process
# 1. Checks if the email exists in the data base - if not return -1
# 2. Checks if the passwords match - if not return 0
# 3. If passed, return 1
def check_login(email, password):
    user = get_user(email.lower())
    if user is None:
        return -1
    if user.password != password:
        return 0
    return 1


def set_session_data(email, password):
    user = get_user(email)
    session['email'] = email
    session['password'] = password
    session['username'] = user.name
    session['location'] = user.location
    session['profileImage'] = user.picture


def clear_session_data():
    session.pop('email', None)
    session.pop('password', None)
    session.pop('username', None)
    session.pop('location', None)
    session.pop('profileImage', None)
