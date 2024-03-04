import os
import re


class Course:
    """
    A class used to represent course

    Attributes
    ----------
    course_id : int
        a unique id for each user
    course_title : str
        title of courses
    course_image_100x100: str
        a link related to course image
    course_headline: str
        headline of course
    course_num_subscribers: int
        the amount of subscribers
    course_avg_rating: float
        the average rating of the course
    course_content_length: float
        the length of the course
    """

    def __init__(self, course_id=-1, course_title='', course_image_100x100='', course_headline='', course_num_subscribers=-1, course_avg_rating=-1.0, course_content_length=-1.0):
        self.course_id = course_id
        self.course_title = course_title
        self.course_image_100x100 = course_image_100x100
        self.course_headline = course_headline
        self.course_num_subscribers = course_num_subscribers
        self.course_avg_rating = course_avg_rating
        self.course_content_length = course_content_length

    @staticmethod
    def find_course_by_title_keyword(keyword):
        """
        To find course based on provided keyword

        This function read course.txt and use regex
        to match required info and return list of tuples
        and create a list of course object

        Parameters
        ----------
        keyword : str
            keyword used to match info

        Returns
        -------
        result_list : list
            a list of course objects

        Examples
        --------

        """
        # go to the file directory
        os.chdir('data/result')
        # initialize result list
        result_list = []
        # open the file and read
        with open('course.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        # have the pattern to match all info needed and have 7 groups
        pattern = re.compile(r'([\d]+);;;([^\n]*?' + keyword + r'[\s\S]*?);;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?)\n', re.IGNORECASE)
        # there are multiple groups so it returns as tuple. (if there is only one group it returns string.Multiple matched String would be a list of string.Now it would be a list of tuple)
        course_list = pattern.findall(data)
        # get to each tuple of the list
        for course in course_list:
            # create the object by accessing to each element of the tuple which contains the exact corresponding info that you extracted from the file in 7 groups
            course = Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6])
            # add them to the result list.
            result_list.append(course)
        return result_list

    @staticmethod
    def find_course_by_id(course_id):
        """
        To find course based on provided id

        This function read course.txt and use regex
        to match required info and return a tuples
        and return the object

        Parameters
        ----------
        course_id : str
            course_id used to match info

        Returns
        -------
        course : object
            a course object

        Examples
        --------

        """
        # go to the file directory
        os.chdir('data/result')
        # open the file and read
        with open('course.txt', 'r', encoding='utf8') as file:
            data = file.read()
            # have the pattern to match all info needed and have 7 groups
            pattern = re.compile(r'(' + course_id + r');;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?)\n')
            course = pattern.search(data)
        os.chdir('..')
        os.chdir('..')
        if not bool(course):
            return None
        else:
            # create the object by accessing to each group of the search which contains the exact corresponding info that you extracted from the file in 7 groups
            course = Course(course.group(1), course.group(2), course.group(3), course.group(4), course.group(5), course.group(6), course.group(7))
            return course

    @staticmethod
    def find_course_by_instructor_id(instructor_id):
        """
        To find course based on provided id

        This function read instructor.txt and use regex
        to match required info and return list of tuples
        and create a list of instructro object

        Parameters
        ----------
        instructor_id : str
            keyword used to match info

        Returns
        -------
        result_list : list
            a list of course objects

        Examples
        --------

        """
        # go to the file directory
        os.chdir('data/result')
        # initialize result list
        result_list = []
        # open the file and read
        with open('user_instructor.txt', 'r', encoding='utf8') as file:
            data = file.read()
            # have the pattern to match the info needed and have 1 group of number
            pattern = re.compile(instructor_id + r'[\s\S]*?([\d-]*?)\n')
            # Since there would be only one matched info I will use search to get string
            course_info = pattern.search(data)
            # have the course list by split the string group1
            course_list = course_info.group(1).split('--')
        # get back to the home otherwise calling another function resulting in error. should always get back as long as you finished opening file.
        os.chdir('..')
        os.chdir('..')
        # have each course id to search it by calling find course by id function. we've already got the course_list indentation is not needed.
        for course_id in course_list:
            # append all found objects to the result list
            result = Course.find_course_by_id(course_id)
            result_list.append(result)
        return result_list

    @staticmethod
    def courses_overview():
        """
        To view the general course info

        This function read course.txt and use regex
        to match required info and return list of tuples
        and create a list of course object

        Parameters
        ----------


        Returns
        -------
        length of course : int
            the amount of courses

        Examples
        --------

        """
        os.chdir('data/result')
        with open('course.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        pattern = re.compile(r'\n')
        course = pattern.findall(data)
        return len(course)

    def __str__(self):
        return str(self.course_id) + ';;;' + str(self.course_title) + ';;;' + str(self.course_image_100x100) + ';;;' + str(self.course_headline) + ';;;' + str(self.course_num_subscribers) + ';;;' + str(self.course_avg_rating) + ';;;' + str(self.course_content_length)


