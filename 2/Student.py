from User import User
import re
import os


class Student(User):
    """
    A subclass used to represent student

    Attributes
    ----------
    user_id : int
        an unique id for each user
    username : str
        a name of each user which would be used to log in.
    password : str
        password used to log in
    user_title: str
        student name
    user_image_50x50: str
        a website linked to the image of instructor
    user_initials: str
        used to create password
    review_id: int
        reviews left by this student

    """

    def __init__(self, user_id=-1, username="", password="", user_title='', user_image_50x50='', user_initials='', review_id=-1):
        super().__init__(user_id, username, password)
        self.user_title = user_title
        self.user_image_50x50 = user_image_50x50
        self.user_initials = user_initials
        self.review_id = review_id

    def view_courses(self, args=[]):
        """
        To find course based on provided list

        This function open student.txt file and
        match the info by regex then print it out

        Parameters
        ----------
        args : list
            not used

        Returns
        -------

        Examples
        --------

        """
        os.chdir('data/result')
        with open('user_student.txt', 'r') as file:
            data = file.read()
        pattern = re.compile(self.user_id + '')
        course_list = pattern.findall(data)
        for course in course_list:
            print(course)
        os.chdir('..')
        os.chdir('..')

    def view_reviews(self, args=[]):
        """
        To find course based on provided list

        This function open student.txt file and
        match the info by regex then print it out

        Parameters
        ----------
        args : list
            not used

        Returns
        -------

        Examples
        --------

        """
        os.chdir('data/result')
        with open('user_student.txt', 'r') as file:
            data = file.read()
        pattern = re.compile(self.user_id + '')
        review_list = pattern.findall(data)
        for review in review_list:
            print(review)
        os.chdir('..')
        os.chdir('..')

    def __str__(self):
        return super(Student, self).__str__() + ';;;' + self.user_image_50x50 + ';;;' + self.user_initials + ';;;' + self.review_id

