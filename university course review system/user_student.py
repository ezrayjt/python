"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""

from math import ceil
from model.user import User
from lib.helper import user_data_path

class Student(User):
    """
    Description: This class is for the manipulation student users.
    And it is inherited from the User class.
    """
    # constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student", email=""):
        User.__init__(self, uid, username, password, register_time, role)
        self.email = email

    # reload the print function
    def __str__(self):
        return f"{self.uid};;;{self.username};;;{self.encrypt_password(self.password)};;;{self.register_time};;;{self.role};;;{self.email}"

    # return a list of students based on the page number and the number of students per page
    # and return the total page number of the students and the total number of students
    def get_students_by_page(self, page):
        # load data
        student_list = []
        with open(user_data_path, 'r') as file:
            for line in file:
                line = line.strip().split(';;;')
                # filter out the students
                if line[4] == 'student':
                    # convert the data into student objects
                    student_list.append(Student(line[0], line[1], line[2], line[3], line[4], line[5]))

        # to get the correct number of students per page, the total page number, and the total number of students
        if page * 20 > len(student_list):
            return (student_list[(page - 1) * 20:], ceil(len(student_list) / 20), len(student_list))
        else:
            return (student_list[(page - 1) * 20:page * 20], ceil(len(student_list) / 20), len(student_list))
        
    # return a student object based on the input id
    def get_student_by_id(self, id):
        # load data
        with open(user_data_path, 'r') as file:
            for line in file:
                line = line.strip().split(';;;')
                # find the correct record according to the id
                if line[0] == str(id):
                    # return the student object
                    return Student(int(line[0]), line[1], line[2], line[3], line[4], line[5])

    # return True if the student is deleted correctly, or return False
    def delete_student_by_id(self, id):
        result = False
        # load data
        with open(user_data_path, 'r') as file:
            # convert the data into a list
            users = [line.strip().split(';;;') for line in file.readlines()]
        # prepare to rewrite the data
        with open(user_data_path, 'w') as new_file:
            for line in users:
                # skip the record that is the target to be deleted
                if line[0] == str(id):
                    result = True
                    continue
                # write other data into the new file
                new_file.write(';;;'.join(line) + '\n')
        return result
