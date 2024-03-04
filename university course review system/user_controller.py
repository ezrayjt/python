"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""
from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()

@user_page.route("/login")
def login():
    return render_template("00login.html")   

@user_page.route("/login", methods=["POST"])
def login_post():
    # Get “username”, “password” values from the request.values.
    req = request.values
    username = req["username"] if "username" in req else ""
    password = req["password"] if "password" in req else ""

    # Use the user validation methods to check the username and password. 
    # If all valid, call the authentication method. 
    if not model_user.validate_username(username):
        return render_err_result(msg="please input correct username")
    if not model_user.validate_password(password):
        return render_err_result(msg="please input correct password")
    # If username and password belong to a valid user, return the string info of this user. 
    # Then, generate a corresponding user object using the generate_user() method 
    # and assign this user to the User.current_login_user class variable.
    login_result, login_info = model_user.authenticate_user(username, password)
    if login_result:
        user_info = generate_user(login_info)
        User.current_login_user = user_info
        return render_result(msg='Login Success.')
    else:
        return render_err_result(msg="Invalid username or password.")

def generate_user(login_user_str):
    login_user = None # a User object
    user_info = login_user_str.strip().split(";;;")
    if user_info[4] == "admin":
        login_user = Admin(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4])
    elif user_info[4] == "instructor":
        login_user = Instructor(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], 
        user_info[5], user_info[6], user_info[7], user_info[8])
    elif user_info[4] == "student":
        login_user = Student(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5])
    return login_user

@user_page.route("/logout")
def logout():
    User.current_login_user = None
    return render_template("01index.html")




@user_page.route("/register")
def register():
    return render_template("00register.html")

@user_page.route("/register", methods=["POST"])
def register_post():
    req = request.values
    username = req["username"] if "username" in req else ""
    password = req["password"] if "password" in req else ""
    email = req["email"] if "email" in req else ""
    register_time = req["register_time"] if "register_time" in req else ""
    role = req["role"] if "role" in req else ""
    if not model_user.validate_username(username):
        return render_err_result(msg="please input correct username")
    if not model_user.validate_password(password):
        return render_err_result(msg="please input correct password")
    if not model_user.validate_email(email):
        return render_err_result(msg="please input correct email")
    
    register_result = model_user.register_user(username, password, email, register_time, role)
    if register_result:
        return render_result(msg="Register Success.")
    else:
        return render_err_result(msg="Register Failed.")

# use @user_page.route("") for each page url

@user_page.route("/student-list")
def student_list():
    if User.current_login_user:
        req = request.values
        page = req["page"] if "page" in req else 1
        context = {}

        one_page_student_list, total_pages, total_num = model_student.get_students_by_page(int(page))
        page_num_list = model_course.generate_page_num_list(int(page), total_pages)

        context['one_page_user_list'] = one_page_student_list
        context['total_pages'] = total_pages
        context['total_num'] = total_num
        context['page_num_list'] = page_num_list
        context['current_page'] = page
        context['current_user_role'] = User.current_login_user.role
    else:
        return redirect(url_for("user_page.login"))
    return render_template("10student_list.html", **context)

@user_page.route("/student-info")
def student_info():
    context = {}
    req = request.values
    student_id = req["id"] if "id" in req else ""
    
    if student_id == "":
        student = User.current_login_user
    else:
        student = model_student.get_student_by_id(str(student_id))
    context['id'] = student.uid
    context['username'] = student.username
    context['password'] = student.password
    context['email'] = student.email
    context['current_user_role'] = student.role
    return render_template("11student_info.html", **context)

@user_page.route("/student-delete")
def student_delete():
    req = request.values
    student_id = req["id"] if "id" in req else ""
    result = model_student.delete_student_by_id(int(student_id))
    if result:
        return redirect(url_for("user_page.student_list"))
    else:
        return redirect(url_for("index_page.index"))
    