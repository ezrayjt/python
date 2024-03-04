"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""

from model.user import User
from lib.helper import user_data_path

class Admin:
    """
    Description: This class is for admin users to register.
    """
    # constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="admin"):
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role

    # this function is to register a new admin user
    def register_admin(self):
        user = User()
        # encrypt password
        self.password = user.encrypt_password(self.password)
        # write to file
        admin = Admin(self.uid, self.username, self.password, self.register_time, self.role)
        with open(user_data_path, 'a') as f:
            f.write(str(admin) + '\n')

    # reload print function
    def __str__(self):
        return f"{str(self.uid)};;;{self.username};;;{self.password};;;{self.register_time};;;{self.role}"