import os
import re


class Review:
    """
    A class used to represent review

    Attributes
    ----------
    course_id : int
        a unique id for each course
    review_id : int
        a unique id for each review
    content: str
        the content of the review
    rating: float
        the average rating of the course
    """
    def __init__(self, review_id=-1, content='', rating=-1.0, course_id=-1):
        self.review_id = review_id
        self.content = content
        self.rating = rating
        self.course_id = course_id

    @staticmethod
    def find_review_by_id(review_id):
        """
        To find review based on provided id

        This function read review_Data.txt and use regex
        to match required info and return tuples
        and create a review object

        Parameters
        ----------
        review_id : str
            keyword used to match info

        Returns
        -------
        review : object
             review objects

        Examples
        --------

        """
        os.chdir('data/result')
        with open('review_data.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        # have the pattern to match all info needed and have 4 groups
        pattern = re.compile(r'(' + review_id + r');;;([\s\S]*?);;;([\s\S]*?);;;([\s\S]*?)\n')
        review = pattern.search(data)
        if not bool(review):
            return None
        else:
            # create the object by accessing to each group of the search which contains the exact corresponding info that you extracted from the file in 7 groups
            review = Review(review.group(1), review.group(2), review.group(3), review.group(4))
            return review

    @staticmethod
    def find_review_by_keywords(keyword):
        """
        To find review based on provided keyword

        This function read review_Data.txt and use regex
        to match required info and return tuples
        and create a review object

        Parameters
        ----------
        keyword : str
            keyword used to match info

        Returns
        -------
        result_list: list
             a list of review objects

        Examples
        --------

        """
        # go to the file directory
        os.chdir('data/result')
        # initialize result list
        result_list = []
        # open the file and read
        with open('review_data.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        # have the pattern to match all info needed and have 4 groups
        pattern = re.compile(r'([\d]+);;;([^\n]*?' + keyword + r'[\s\S]*?);;;([\s\S]*?);;;([\s\S]*?)\n', re.IGNORECASE)
        # there are multiple groups so it returns as tuple. (if there is only one group it returns string.Multiple matched String would be a list of string.Now it would be a list of tuple)
        review_list = pattern.findall(data)
        # get to each tuple of the list
        for review in review_list:
            # create the object by accessing to each element of the tuple which contains the exact corresponding info that you extracted from the file in 7 groups
            review = Review(review[0], review[1], review[2], review[3])
            # add them to the result list.
            result_list.append(review)
        return result_list

    @staticmethod
    def find_review_by_course_id(course_id):
        """
        To find review based on provided id

        This function read review_Data.txt and use regex
        to match required info and return tuples
        and create a review object

        Parameters
        ----------
        course_id : str
            keyword used to match info

        Returns
        -------
        result_list: list
             a list of review objects

        Examples
        --------

        """
        # go to the file directory
        os.chdir('data/result')
        # initialize result list
        result_list = []
        # open the file and read
        with open('review_data.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        # have the pattern to match all info needed and have 4 groups
        pattern = re.compile(r'([\d]+);;;([\w\W].*?);;;(.*?);;;(' + str(course_id) + r')\n')
        # there are multiple groups so it returns as tuple. (if there is only one group it returns string.Multiple matched String would be a list of string.Now it would be a list of tuple)
        review_list = pattern.findall(data)
        # get to each tuple of the list
        for review in review_list:
            # create the object by accessing to each element of the tuple which contains the exact corresponding info that you extracted from the file in 7 groups
            review = Review(review[0], review[1], review[2], review[3])
            # add them to the result list.
            result_list.append(review)
        return result_list

    @staticmethod
    def reviews_overview():
        """
        To find review based on provided keyword

        This function read review_Data.txt and use regex
        to match required info and return tuples
        and create a review object

        Parameters
        ----------


        Returns
        -------
        length of reviews: int
             the amount of reviews

        Examples
        --------

        """
        os.chdir('data/result')
        # it only scans the content and store it to the variable data then close the file. done.
        with open('review_data.txt', 'r', encoding='utf8') as file:
            data = file.read()
        os.chdir('..')
        os.chdir('..')
        # since we've already got data,it's unnecessary to have later part intended to be within 'open'.
        pattern = re.compile(r'\n')
        reviews = pattern.findall(data)
        return str(len(reviews))

    def __str__(self):
        # just convert everything to str in case it pops out that int couldn't add to str e.t.
        return str(self.review_id) + ';;;' + str(self.content) + ';;;' + str(self.rating) + ';;;' + str(self.course_id)



