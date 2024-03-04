from User import User
from Course import Course
from Review import Review


class Instructor(User):
    """
    A subclass used to represent Instructor

    Attributes
    ----------
    user_id : int
        an unique id for each user
    username : str
        a name of each user which would be used to log in.
    password : str
        password used to log in
    job_title: str
        the job of the instructor
    image_100x100: str
        a website linked to the image of instructor
    course_id_list: str
        course taught by this instructor
    display_name: str
        how the instructor name displays.
    """

    def __init__(self, user_id=-1, username="", password="", display_name='', job_title='', image_100x100='', course_id_list=[]):
        super().__init__(user_id, username, password)
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id_list = course_id_list
        self.display_name = display_name

    def view_courses(self, args=[]):
        """
        To find course based on provided keyword

        This function call the function from courser class and
        print the info

        Parameters
        ----------
        args : list
            keyword used to match info

        Returns
        -------

        Examples
        --------

        """
        # cuz [0:10] would not influence the result if element is less than 10.It only works when it's more than 10
        for x in Course.find_course_by_instructor_id(self.user_id)[0:10]:
            print(x)

    def view_reviews(self, args=[]):
        """
        To find review based on provided keyword

        This function call the function from review class and
        print the info

        Parameters
        ----------

        Returns
        -------

        Examples
        --------

        """
        # passed in the instructor id and get a course object list.
        for x in Course.find_course_by_instructor_id(self.user_id):
            print(x)
            # each x is an object. we should access its id then pass it.otherwise it's info contains everything about the course.
            for y in Review.find_review_by_course_id(x.course_id):
                print(y)

    def __str__(self):
        return super(Instructor, self).__str__() + str(self.display_name) + ';;;' + str(self.job_title) + ';;;' + str(self.image_100x100) + ';;;' + str(self.course_id_list)


