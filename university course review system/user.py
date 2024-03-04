"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""

import random
from lib.helper import user_data_path, course_data_path, course_json_files_path

class User:
    """
    Description: This class is for basic functions, such as check validation of infos and
    authentication, for all users' usage.
    """
    # class variable
    current_login_user = None
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role=""):
        # constructor
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role

    def __str__(self):
        # reload print
        return f"{self.uid};;;{self.username};;;{self.password};;;{self.register_time};;;{self.role}"

    # return True and the info of the user if the authentication is valid, or return False and ""
    def authenticate_user(self, username, password): 
        # load data
        with open(user_data_path) as f:
            for line in f:
                # convert the format
                user = line.strip().split(";;;")
                # to check if the username and password matched
                if username == user[1] and self.encrypt_password(password) == user[2]:
                    return (True, line)

        return (False, "")

    # return True if the name exists in the file or False otherwise
    def check_username_exist(self, username):
        # load data
        with open(user_data_path) as f:
            for line in f:
                # convert the format
                user = line.strip().split(";;;")
                # check if exists
                if username == user[1]:
                    return True
        return False
    
    # return a unique user id which is different from all ids in the user file
    def generate_unique_user_id(self):
        # using a loop to continue generate a random id
        # till the id never exists in the user file
        while True:
            # generate id
            uid = random.randint(100000, 999999)
            # load file
            with open(user_data_path) as f:
                for line in f:
                    user = line.strip().split(";;;")
                    # check if the id exists
                    if int(user[0]) == uid:
                        continue
                break
        return uid

    # return a encrypted password according to the input password
    def encrypt_password(self, password):
        # This function is from Assessment 2
        # This is for encrypting the password for users
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

        encrypted_info = '^^^'
        for i in range(len(password)):
            if i % 3 == 0:
                position = len(password) % len(all_punctuation)
                character = all_punctuation[position]
                encrypted_info = encrypted_info + character + password[i] + character
            elif i % 3 == 1:
                position = len(password) % 5
                character = all_punctuation[position]
                encrypted_info = encrypted_info + character*2 + password[i] + character*2
            elif i % 3 == 2:
                position = len(password) % 10
                character = all_punctuation[position]
                encrypted_info = encrypted_info + character*3 + password[i] + character*3

        encrypted_info += '$$$'

        return encrypted_info

    # return True if the user is registered successfully or False otherwise
    def register_user(self, username, password, email, register_time, role):
        # call check username exist function to validate the username
        if self.check_username_exist(username):
            return False
        
        # generate id, encrypt the password, and convert the date by calling predefined functions
        uid = self.generate_unique_user_id()
        encrypted_password = self.encrypt_password(password)
        register_time = self.date_conversion(register_time)

        # open the file and write down the user according to the role of the user
        with open(user_data_path, "a") as f:
            if role == 'instructor':
                f.write(f"{str(uid)};;;{username};;;{encrypted_password};;;{register_time};;;{role};;;{email};;;;;;;;;\n")
            elif role == 'student':
                f.write(f"{str(uid)};;;{username};;;{encrypted_password};;;{register_time};;;{role};;;{email}\n")
        return True

    # this function is used to convert a unix epoch timestamp(register_time) to a string with format "yyyy-MM-dd_HH:mm:ss.SSS"
    def date_conversion(self, register_time):
        # Human Readable Time	        Seconds
        # 1 Hour	                    3600 Seconds
        # 1 Day	                        86400 Seconds
        # 1 Week	                    604800 Seconds
        # 1 Month	                    2629743 Seconds
        # 1 Year 	                    31556926 Seconds

        # test time here https://www.unixtimestamp.com/index.php

        # melbourne time is GMT+11
        
        # your code
        # reference https://www.geeksforgeeks.org/convert-unix-timestamp-to-dd-mm-yyyy-hhmmss-format/
        ans = ""

        # Number of days in month
        # in normal year
        daysOfMonth = [ 31, 28, 31, 30, 31, 30,
                        31, 31, 30, 31, 30, 31 ]

        (currYear, daysTillNow, extraTime,
            extraDays, index, date, month, hours,
            minutes, secondss, flag) = ( 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0 )

        # Calculate total days unix time T
        register_time = int(register_time)
        daysTillNow = register_time // (24 * 60 * 60 * 1000)
        extraTime = register_time % (24 * 60 * 60 * 1000)
        currYear = 1970

        # Calculating current year
        while (daysTillNow >= 365):
            if (currYear % 400 == 0 or
                (currYear % 4 == 0 and
                currYear % 100 != 0)):
                daysTillNow -= 366
                
            else:
                daysTillNow -= 365
                
            currYear += 1
                
        # Updating extradays because it
        # will give days till previous day
        # and we have include current day
        extraDays = daysTillNow + 1

        if (currYear % 400 == 0 or
            (currYear % 4 == 0 and
            currYear % 100 != 0)):
            flag = 1

        # Calculating MONTH and DATE
        month = 0
        index = 0
            
        if (flag == 1):
            while (True):

                if (index == 1):
                    if (extraDays - 29 < 0):
                        break
                        
                    month += 1
                    extraDays -= 29
                    
                else:
                    if (extraDays - daysOfMonth[index] < 0):
                        break
                        
                    month += 1
                    extraDays -= daysOfMonth[index]
                    
                index += 1
                
        else:
            while (True):
                if (extraDays - daysOfMonth[index] < 0):
                    break
                    
                month += 1
                extraDays -= daysOfMonth[index]
                index += 1

        # Current Month
        if (extraDays > 0):
            month += 1
            date = extraDays
            
        else:
            if (month == 2 and flag == 1):
                date = 29
            else:
                date = daysOfMonth[month - 1]

        # Calculating HH:MM:YYYY
        hours = extraTime // (3600 * 1000)
        minutes = (extraTime % (3600 * 1000)) // (60 * 1000)
        secondss = (extraTime % (3600 * 1000)) % (60 * 1000) / 1000

        ans += str(currYear)
        ans += "-"
        ans += str(month)
        ans += "-"
        ans += str(date)
        ans += " "
        ans += "{:0>2d}".format(hours + 11)
        ans += ":"
        ans += "{:0>2d}".format(minutes)
        ans += ":"
        ans += "{}".format(secondss)

        # Return the time
        ans
        return ans

    # return True if the username is only made by alphabets and underscores
    def validate_username(self, username):
        # remove the underscores
        username = username.replace("_", "")
        # check if the rest of the username is made of alphabets only
        if not username.isalpha():
            return False
        return True

    # return True if the length of password is not less than 5 or false otherwise
    def validate_password(self, password):
        if len(password) < 5:
            return False
        return True

    # return True if the email address is in the correct format or False otherwise
    def validate_email(self, email):
        # check the length of email address
        if len(email) <= 8:
            return False
        # check if the email address ends with .com
        if not email.endswith(".com"):
            return False
        # check if the email address contains @
        if email.count("@") != 1:
            return False
        return True

    # cleare the user data file
    def clear_user_data(self):
        with open(user_data_path, "w") as f:
            f.write("")




