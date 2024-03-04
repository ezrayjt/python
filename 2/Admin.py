import re
import os
from User import User
from Course import Course
from Review import Review


class Admin(User):
    """
    A subclass used to represent Admin

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
        super().__init__(user_id, username, password)

    def register_admin(self):
        """
        To check if the admin exist or not and store it in the admin.txt.

        This function create a file named admin.txt at the first time runing this
        function.Then check the object existence in the file.If it doesn't exit
        write it into the file.

        Parameters
        ----------

        self : Admin
            Admin object

        Returns
        -------

        Examples
        --------

        """
        # have a boolean variable to support the check functionality
        found = False
        # have a list to store info in the txt file.
        user_admin_list = []
        # change the directory to the result file
        os.chdir('data/result')
        # create the user_admin file at the first time when it doesn't exist.
        with open('user_admin.txt', 'a'):
            pass
        # read the file to check if the name exists or not and append.
        with open('user_admin.txt', 'r+') as file:
            # read the content of the file
            for line in file:
                # make the content a list.
                user_admin_list = line.split(';;;')
            # check if the name exist
            for name in user_admin_list:
                if name == self.username:
                    found = True
            if not found:
                # append the username at the end of the file with ";;;" in the front. convert object to string.
                file.write(str(self.user_id) + ';;;' + str(self.username) + ';;;' + User.encryption(str(self.password)) + '\n')

        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def extract_course_info():
        """
        To extract info from raw data

        This function read the raw_data.txt and use regular expression to match
        required info and then write it to a new file.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        # get to raw_data directory.
        os.chdir('data/course_data')
        # open raw_data file
        with open('raw_data.txt', 'r', encoding='utf8') as file:
            # read the content of the file and save it to variable data
            data = file.read()
            # set the pattern to match course id
            pattern = re.compile(r'\"course\",\"id\":(\d+)')
            # get the list of the course id
            course_id = pattern.findall(data)

            # set the pattern to match course title
            pattern = re.compile(r'\"course\",\"id\":\d+,\"title\":\"([\s\S]*?)\"')
            # get the list of the course title
            course_title = pattern.findall(data)
            # add ';;;' to the beginning of each element to meet the requirement of file format
            course_title = [';;;' + x for x in course_title]

            # set the pattern to match image
            pattern = re.compile(r'\"image_100x100\":\"([\w./:-]+cou\w*?/100x100[^\"]+)')
            # get the list of the image
            image = pattern.findall(data)
            # add ';;;' to the beginning of each element to meet the requirement of file format
            image = [';;;' + x for x in image]

            # set the pattern to match headline
            pattern = re.compile(r'\"headline\":\"([\s\S]*?)\",\"')
            # get the list of the headline
            headline = pattern.findall(data)
            # add ';;;' to the beginning of each element to meet the requirement of file format
            headline = [';;;' + x for x in headline]

            # same process to num_of_subscribers,avg_rating and course_content_length
            pattern = re.compile(r'"num_subscribers":(\d+)')
            num_of_subscribers = pattern.findall(data)
            num_of_subscribers = [';;;' + x for x in num_of_subscribers]

            pattern = re.compile(r'"avg_rating":([\d.]+)')
            avg_rating = pattern.findall(data)
            avg_rating = [';;;' + x for x in avg_rating]

            pattern = re.compile(r'"content_info":"([\d.]+)')
            course_content_length = pattern.findall(data)
            course_content_length = [';;;' + x for x in course_content_length]

            # initialize a new list course_txt which will contain all information which will be converted to the txt file.
            course_txt = []
            i = 0
            # there are 3200 items in total . use while loop to iterate for 3200 times
            while i < 3200:
                # have the element course by adding through matched element of course id list and course title list from 1 to 3200
                course_element = course_id[i] + course_title[i] + image[i] + headline[i] + num_of_subscribers[i] + avg_rating[i] + course_content_length[i]
                # add new matched elements(course id and course title) to the new list
                course_txt.append(course_element)
                i += 1
        # so there would be a new line at the last. It would be convenient for later regex.
        course_txt.append('')
        # add new line to the end of each element and store the extracted info to the course_file variable in order to write it later after changing the working directory to the expected file
        course_file = '\n'.join(course_txt)

        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')
        # change the directory to the result file
        os.chdir('data/result')

        # create and write the extracted information to course file.
        with open('course.txt', 'w', encoding='utf8') as file:
            file.write(course_file)

        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def extract_review_info():
        """
        To extract info from raw data

        This function read the review_data.txt and use regular expression to match
        required info and then write it to a new file.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        # get to the review_data folder
        os.chdir('data/review_data')
        # have a for loop to get through all files in the folder
        for filename in os.listdir():
            # open each file
            with open(filename, 'r', encoding='utf8') as file:
                # scan and save the file content to data.
                data = file.read()
                # have the pattern to get review id.
                pattern = re.compile(r'"course_review", "id":[ ]?([\d]+)')
                # have the review id list
                review_id = pattern.findall(data)

                # the same with the review id
                pattern = re.compile(r'"course_review", "id": .*?content": "([\s\S]*?)",')
                review_content = pattern.findall(data)
                # add ;;; at the beginning to meet the requirement of the assignment
                review_content = [';;;' + x for x in review_content]

                pattern = re.compile(r'"rating":[ ]*?([\d.]+)')
                review_rating = pattern.findall(data)
                review_rating = [';;;' + x for x in review_rating]

                # get the course_id(the id would change automatically through the for loop),and add ;;; , remove '.jason' to meet the requirement
                course_id = ';;;' + file.name[:-5]

                # initialize the review data list
                review_data = []
                # have the while loop to
                i = 0
                while i < len(review_id):
                    # only the course_id is different from former functions cuz for each file the course_id is the same.
                    review_element = review_id[i] + review_content[i] + review_rating[i] + course_id
                    review_data.append(review_element)
                    i += 1
            # have to add one empty element in the end.If not,when it gets to another file,it started from the end of the data.then it lacks one new line
            review_data.append('')
            review_file = '\n'.join(review_data)

            # get back to the original directory.
            os.chdir('..')
            os.chdir('..')
            # change the directory to the result file
            os.chdir('data/result')

            with open('review_data.txt', 'a') as file:
                file.write(review_file)

            # get back to review data here because we are in for loop if we don't do this the start of for loop can't get the file.
            os.chdir('..')
            os.chdir('..')
            os.chdir('data/review_data')

        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def extract_students_info():
        """
        To extract info from raw data

        This function read the raw_data.txt and use regular expression to match
        required info and then write it to a new file.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        # have the id list of instructor and admin
        os.chdir('data/result')
        # get the info of files
        with open('user_instructor.txt', 'r', encoding='utf8') as file:
            user_instructor = file.read()
        with open('user_admin.txt', 'r', encoding='utf8') as file:
            user_admin = file.read()
        # It's done. get back to the review data
        os.chdir('..')
        os.chdir('..')
        os.chdir('data/review_data')
        # get the id list of instructor id.
        pattern = re.compile(r'([\d]+);;;[\s\S]*?\n')
        user_instructor_list = pattern.findall(user_instructor)
        # get the id list of admin id
        pattern = re.compile(r'([\d]+);;;[\s\S]*?\n')
        user_admin_list = pattern.findall(user_admin)
        # have a student_id_list to store all student id to check if new generated one exists.
        student_id_list = []
        for filename in os.listdir():
            with open(filename, 'r', encoding='utf8') as file:
                data = file.read()
                # we have to put review id in the beginning to use it as standard to check if id is missed
                pattern = re.compile(r'"course_review", "id":[ ]?([\d]+)')
                review_id = pattern.findall(data)
                review_id = [';;;' + x for x in review_id]

                pattern = re.compile(r'course_review"[\s\S]*?"user", "id": ([\d]+)')
                student_id = pattern.findall(data)
                for x in student_id:
                    student_id_list.append(x)
                # to see how many student id is missed in this file.
                if len(student_id) != len(review_id):
                    # have to store len student id here. if you have len(r_id) - len(s_id) s_id list append and it will add less
                    j = len(student_id)
                    i = 0
                    # add certain amount of student id equaling to the length of review id list.
                    while i < len(review_id) - j:
                        unique_id = User.generate_unique_user_id(user_admin_list + user_instructor_list + student_id_list)
                        # get student id appended new ids.
                        student_id.append(unique_id)
                        i += 1

                pattern = re.compile(r'"course_review"[\s\S]*?"title": "([\s\S]+?)", "')
                user_inter = pattern.findall(data)
                username = [';;;' + re.sub('\s+', '_', x).lower() for x in user_inter]
                user_title = [';;;' + x for x in user_inter]

                pattern = re.compile(r'"course_review"[\s\S]*?"image_50x50": "([\s\S]+?)", "')
                user_image = pattern.findall(data)
                user_image = [';;;' + x for x in user_image]

                pattern = re.compile(r'"course_review"[\s\S]*?"initials": "([\s\S]+?)"}')
                user_init = pattern.findall(data)
                user_initials = [';;;' + x for x in user_init]

                # get password by list comprehension
                password_raw = [user_init[i].lower() + student_id[i] + user_init[i].lower() for i in range(0, len(user_init))]
                # initialize password list
                password_list = []
                # call the encryption function
                for x in password_raw:
                    # call the encryption function to get the password and format it
                    password = ';;;' + User.encryption(x)
                    # have it in the password list.
                    password_list.append(password)

                student_data = []
                i = 0
                while i < len(review_id):
                    student_element = student_id[i] + username[i] + password_list[i] + user_title[i] + user_image[i] + user_initials[i] + review_id[i]
                    student_data.append(student_element)
                    i += 1
            student_data.append('')
            student_file = '\n'.join(student_data)

            # get back to the original directory.
            os.chdir('..')
            os.chdir('..')
            # change the directory to the result file
            os.chdir('data/result')

            with open('user_student.txt', 'a') as file:
                file.write(student_file)

            # get back to review data here because we are in for loop if we don't do this the start of for loop can't get the file.
            os.chdir('..')
            os.chdir('..')
            os.chdir('data/review_data')

        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def extract_instructor_info():
        """
        To extract info from raw data

        This function read the raw_data.txt and use regular expression to match
        required info and then write it to a new file.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        # get to raw_data directory.
        os.chdir('data/course_data')
        # open raw_data file
        with open('raw_data.txt', 'r', encoding='utf8') as file:
            # read the content of the file and save it to variable data
            data = file.read()
        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')
        # set the pattern to match instructor id
        pattern = re.compile(r'"visible_instructors"[\w\W]*?"id":([\d]*?),')
        # get the list of the instructor_id
        instructor_id = pattern.findall(data)
        # initialize password list.
        password_list = []
        # use for loop to get through each id in the list. x is id.
        for x in instructor_id:
            # call the encryption function to get the password and format it
            password = ';;;' + User.encryption(x)
            # have it in the password list.
            password_list.append(password)
        # add an element to the list in order to check if it exists or not.
        instructor_id.insert(0, '')

        # set the pattern to match instructor_name
        pattern = re.compile(r'"visible_instructors":[\w\W]*?"display_name":"([\s\S]*?)","')
        # get the list of the instructor_name
        display_name = pattern.findall(data)
        # use list comprehension to replace space by under-score. x is the string element of the list.
        username = [';;;' + re.sub('\s+', '_', x).lower() for x in display_name]
        # formatting display_name
        display_name = [';;;' + x for x in display_name]

        # same process
        pattern = re.compile(r'"visible_instructors":[\w\W]*?"job_title":"([\s\S]*?)","')
        job_title = pattern.findall(data)
        job_title = [';;;' + x for x in job_title]

        # same process
        pattern = re.compile(r'"visible_instructors":[\w\W]*?"image_100x100":"([\s\S]*?)","')
        image_100x100 = pattern.findall(data)
        # add ;;; at beginning and end of image to have course id clean in order to add it without ;;;
        image_100x100 = [';;;' + x + ';;;' for x in image_100x100]

        # same process
        pattern = re.compile(r'"_class":"course","id":([\d]*?),"[\s\S]*?"visible_instructors"')
        course_id = pattern.findall(data)

        # initialize a new dictionary to locate the same id
        instructor_dic = {}
        # have an instructor_id_list to check if it exists
        instructor_id_list = []
        # have a list to store contents which would be used to convert to the file
        instructor = []
        i = 0
        # there are 3200 items in total . use while loop to iterate for 3200 times
        while i < 3200:
            # the first element is empty of instructor_id. so the first time it would go to else.
            instructor_id_list.append(instructor_id[i])
            # when the next id is in the list . it gets back to the list to modify it
            if instructor_id[i+1] in instructor_id_list:
                # use the dic to locate the same id and modify it
                instructor_dic[instructor_id[i+1]] += '--' + course_id[i]
            # the instructor id didn't repeat , update it to the dic
            else:
                # have all info to a string
                instructor_element = instructor_id[i+1] + username[i] + password_list[i] + display_name[i] + job_title[i] + image_100x100[i] + course_id[i]
                # update the dic
                instructor_dic.update({instructor_id[i+1]: instructor_element})
            i += 1
        # access to the data
        for x in instructor_dic.values():
            instructor.append(x)
        # there would be a new line at the last. It would be convenient for later regex.
        instructor.append('')
        # add new line to the end of each element and store the extracted info to the  variable in order to write it later after changing the working directory to the expected file
        instructor_file = '\n'.join(instructor)

        # change the directory to the result file
        os.chdir('data/result')

        # create and write the extracted information to course file.
        with open('user_instructor.txt', 'w', encoding='utf8') as file:
            file.write(instructor_file)

        # get back to the original directory.
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def extract_info():
        """
        To extract info from files

        This function calls all extraction function

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        Admin.extract_instructor_info()
        Admin.extract_review_info()
        Admin.extract_course_info()
        Admin.extract_students_info()

    @staticmethod
    def remove_data():
        """
        To remove info from files

        This function open all files in result folder
        and overwrite files with blank.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        os.chdir('data/result')
        for filename in os.listdir():
            with open(filename, 'w') as file:
                pass
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def view_courses(args=[]):
        """
        To view course information by different commands

        This function calls functions from course class and
        review class to print required info.

        Parameters
        ----------
        args : list

        Returns
        -------

        Examples
        --------

        """
        if len(args) == 2:
            if args[0] == 'TITLE_KEYWORD':
                # the return is object list so use for loop to print object but not the list
                for x in Course.find_course_by_title_keyword(args[1]):
                    print(x)
            elif args[0] == 'ID':
                # the return is object so print directly
                print(Course.find_course_by_id(args[1]))
            elif args[0] == 'INSTRUCTOR_ID':
                # the return is object list so use for loop to print object but not the list
                for x in Course.find_course_by_instructor_id(args[1]):
                    print(x)
            else:
                print('You didn\'t input  commands to show specific information.System will show the course overview.')
                print(Course.courses_overview())
        else:
            print('You didn\'t input  commands to show specific information.System will show the course overview.')
            print(Course.courses_overview())

    @staticmethod
    def view_reviews(args=[]):
        """
        To view review information by different commands

        This function calls functions from course class and
        review class to print required info.

        Parameters
        ----------
        args : list

        Returns
        -------

        Examples
        --------

        """
        if len(args) == 2:
            if args[0] == 'ID':
                # the return is object so print directly
                print(Review.find_review_by_id(args[1]))
            elif args[0] == 'KEYWORD':
                # the return is object list so use for loop to print object but not the list
                for x in Review.find_review_by_keywords(args[1]):
                    print(x)
            elif args[0] == 'COURSE_ID':
                # the return is object list so use for loop to print object but not the list
                for x in Review.find_review_by_course_id(args[1]):
                    print(x)
                Review.find_review_by_course_id(args[1])
            else:
                print('You didn\'t input  commands to show specific information.System will show the review overview.')
                print(Review.reviews_overview())
        else:
            print('You didn\'t input  commands to show specific information.System will show the review overview.')
            print(Review.reviews_overview())

    @staticmethod
    def view_users():
        """
        To view user information by different commands

        This function calls functions read files in result folder
        and print numbers of each type of users.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        os.chdir('data/result')
        with open('user_admin.txt', 'r', encoding='utf8') as file:
            data = file.read()
        pattern = re.compile(r'\n')
        admin = pattern.findall(data)
        print('Total number of admin: ' + str(len(admin)))
        with open('user_instructor.txt', 'r', encoding='utf8') as file:
            data = file.read()
        pattern = re.compile(r'\n')
        instructor = pattern.findall(data)
        print('Total number of instructor: ' + str(len(instructor)))
        with open('user_student.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        pattern = re.compile(r'\n')
        student = pattern.findall(data)
        print('Total number of student: ' + str(len(student)))

    def __str__(self):
        return super(Admin, self).__str__()

