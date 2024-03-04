import random
import re
import os


class User:
    """
    A class used to represent User

    Attributes
    ----------
    user_id : int
        an unique id for each user
    username : str
        a name of each user which would be used to log in.
    password : str
        password used to log in
    """
    def __init__(self, user_id=-1, username="", password=""):
        self.user_id = user_id
        self.username = username
        self.password = password

    @staticmethod
    def generate_unique_user_id(id_list):
        """
        To generate a random number .

        This function generates a random number
        with 10 digits.And it authenticates generated number's existence within
        the list.

        Parameters
        ----------

        id_list : str
            provided list to be used for verification

        Returns
        -------
        str
            user id which is randomly generated

        Examples
        --------
        >>>generate_user_id(['100','234'])
        '125'
        """
        # generate a random number with asked digits and convert it to string type.
        user_id = str(random.randint(10**9, 10**10-1))
        # check if the number is in the list
        while user_id in id_list:
            # if it is true then generate another new id
            user_id = str(random.randint(10**9, 10**10-1))
        # return id
        return user_id

    @staticmethod
    def encryption(input_str):
        """
        encrypt the password.

        Based on the user input,this function add punctuations to
        the input value by following a certain pattern.

        Parameters
        ----------
        input_str:str
            password gets from user input

        Returns
        -------
        str
            required values after encryption

        Examples
        --------
        >>>encryption('password')
        '^^^)p)$$a$$)))s))))s)$$w$$)))o))))r)$$d$$$$$'
        """
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        # get the first character
        first_character = all_punctuation[len(input_str) % len(all_punctuation)]
        # get the second character
        second_character = all_punctuation[len(input_str) % 5]
        # get the third character
        third_character = all_punctuation[len(input_str) % 10]
        # split password into every 3 letters
        password_list = [input_str[i:i+3] for i in range(0, len(input_str), 3)]
        # initialize password
        password = ''
        # use for loop to edit each 3 letters
        for x in password_list:
            # check the index of the list(x)
            if len(list(x)) == 3:
                # convert each element to list of every letter and then concatenate punctuations and letters
                password += first_character+list(x)[0]+first_character+second_character*2+list(x)[1]+second_character*2+third_character*3+list(x)[2]+third_character*3
            elif len(list(x)) == 2:
                password += first_character+list(x)[0]+first_character+second_character*2+list(x)[1]+second_character*2
            elif len(list(x)) == 1:
                password += first_character+list(x)[0]+first_character
        # add the first and last 3 characters
        password = """^^^""" + password + """$$$"""
        # return the password
        return password

    def login(self):
        """
        Authenticate the username and the password.

        Based on the input object ,this function open files and get data.
        checks if these two values matches in the provided list

        Parameters
        ----------
        self : User
        Returns
        -------
        boolean or tuple
            depend on the authentication of username,password

        Examples
        --------
        >>User.login('aaaa','123',[“aaaa”, “^^^&1&!!2!!&&&3&&&&3&!!3!!$$$”, “aa@gmail.com”, “3151”])
        False,
        """
        # get data from 3 files.
        os.chdir('data/result')
        # create the user_instructor file at the first time if it doesn't exist.
        with open('user_instructor.txt', 'a'):
            pass
        # create the user_student file at the first time if it doesn't exist.
        with open('user_student.txt', 'a'):
            pass
        # create the course file at the first time if it doesn't exist.
        with open('course.txt', 'a'):
            pass
        # create the review_data file at the first time if it doesn't exist.
        with open('review_data.txt', 'a'):
            pass
        with open('user_instructor.txt', 'r', encoding='utf8') as file:
            user_instructor = file.read()
        with open('user_admin.txt', 'r', encoding='utf8') as file:
            user_admin = file.read()
        with open('user_student.txt', 'r', encoding='utf8') as file:
            user_student = file.read()
        # It's done. get back to home
        os.chdir('..')
        os.chdir('..')
        # get the user_list by combining all data got from the files. username and user password is needed.
        pattern = re.compile(r'([\d]+);;;([\s\S]*?);;;([\w\W]*?);;;[\w\W]*?\n')
        # get the list of tuple. within each tuple: tuple[0] is id tuple[1] is name tuple[2] is password
        user_instructor_list = pattern.findall(user_instructor)
        pattern = re.compile(r'([\d]+);;;([\s\S]*?);;;([\w\W]*?);;;[\w\W]*?\n')
        user_student_list = pattern.findall(user_student)
        pattern = re.compile(r'([-\d]+);;;([\s\S]*?);;;([\w\W]*?)\n')
        user_admin_list = pattern.findall(user_admin)
        # have id list to check if input is in and witch list it is in to confirm the role
        user_instructor_id_list = [x[0] for x in user_instructor_list]
        user_student_id_list = [x[0] for x in user_student_list]
        user_admin_id_list = [x[0] for x in user_admin_list]

        # have to convert id to str otherwise it doesn't match.
        if str(self.user_id) in user_instructor_id_list:
            # access to each tuple of user_list
            for x in user_instructor_list:
                # check if username matches
                if str(self.username) == x[1]:
                    # check if password matches
                    if User.encryption(str(self.password)) == x[2]:
                        login_result = (True,)
                        login_user_role = ('Instructor',)
                        login_user_info = login_result + login_user_role + x
                        return login_user_info
                    else:
                        return False,

        elif str(self.user_id) in user_student_id_list:
            for x in user_student_list:
                # check if username matches
                if str(self.username) == x[1]:
                    # check if password matches
                    if User.encryption(str(self.password)) == x[2]:
                        login_result = (True,)
                        login_user_role = ('Student',)
                        login_user_info = login_result + login_user_role + x
                        return login_user_info
                    else:
                        return False,

        elif str(self.user_id) in user_admin_id_list:
            for x in user_admin_list:
                # check if username matches
                if str(self.username) == x[1]:
                    # check if password matches
                    if User.encryption(str(self.password)) == x[2]:
                        login_result = (True,)
                        login_user_role = ('Admin',)
                        login_user_info = login_result + login_user_role + x
                        return login_user_info
                    else:
                        return False,
        else:
            return False,

    @staticmethod
    def extract_info():
        print('You have no permission to extract information')

    @staticmethod
    def view_courses(args=[]):
        print('You have no permission to view courses')

    @staticmethod
    def view_users():
        print('You have no permission to view users')

    @staticmethod
    def view_reviews(args=[]):
        print('You have no permission to view reviews')

    @staticmethod
    def remove_data():
        print('You have no permission to remove data')

    def __str__(self):
        return str(self.user_id) + ';;;' + str(self.username) + ';;;' + str(self.password)

