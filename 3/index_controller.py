"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""
from flask import render_template, Blueprint

from model.user import User
from model.user_admin import Admin


index_page = Blueprint("index_page", __name__)

@index_page.route("/")
def index():
    # check the class variable User.current_login_user
    # If there exists a logged user, pass the current_login_user’s role to context[‘current_user_role’].
    context = {}
    if User.current_login_user:
        context['current_user_role'] = User.current_login_user.role
    # manually register an admin account when open index page
    user = User()
    if not user.check_username_exist('admin'):
        admin = Admin(user.generate_unique_user_id(), 'admin', 'admin')
        admin.register_admin()
    return render_template("01index.html", **context)

