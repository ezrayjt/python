"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""

from math import ceil
from lib.helper import course_json_files_path, course_data_path, user_data_path, figure_save_path
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class Course:
    """
    Description: This class is used to get course information from given json files and manipulate them.
    """
    # constructor
    def __init__(self, category_title="", subcategory_id=-1, subcategory_title="",
    subcategory_description="", subcategory_url="", course_id=-1, course_title="",
    course_url="", num_of_subscribers=0, avg_rating=0.0, num_of_reviews=0):
        self.category_title = category_title
        self.subcategory_id = subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews

    # reload print function
    def __str__(self):
        return f"{self.category_title};;;{self.subcategory_id};;;{self.subcategory_title};;;{self.subcategory_description};;;{self.subcategory_url};;;{self.course_id};;;{self.course_title};;;{self.course_url};;;{self.num_of_subscribers};;;{self.avg_rating};;;{self.num_of_reviews}"

    # extract course information from json files
    def get_courses(self):
        # load data from a nested folder directory
        course_list = []
        for path in os.listdir('.' + course_json_files_path):
            if not path.startswith('.'):
                for category in os.listdir('.' + course_json_files_path + '/' + path):
                    if not category.startswith('.'):
                        for subcategory in os.listdir('.' + course_json_files_path + '/' + path + '/' + category):
                            with open('.' + course_json_files_path + '/' + path + '/' + category + '/' + subcategory, 'r') as f:
                                # read json file using json library
                                data = json.load(f)
                                # extract course information from json file
                                # and store them in a list
                                for unit in data.values():
                                    for item in unit['items']:
                                        category_title = path.split('_')[-1]
                                        subcategory_id = unit['source_objects'][0]['id']
                                        subcategory_title = unit['source_objects'][0]['title']
                                        subcategory_description = unit['source_objects'][0]['description']
                                        subcategory_url = unit['source_objects'][0]['url']
                                        course_id = item['id']
                                        course_title = item['title']
                                        course_url = item['url']
                                        num_of_subscribers = item['num_subscribers']
                                        avg_rating = item['avg_rating']
                                        num_of_reviews = item['num_reviews']
                                        course_list.append([category_title, subcategory_id, subcategory_title, subcategory_description, 
                                        subcategory_url, course_id, course_title, course_url, num_of_subscribers, avg_rating, num_of_reviews])
        
        # write course information into a file
        with open(course_data_path, 'w') as file:
            for line in course_list:
                file.write(';;;'.join([str(i) for i in line]) + '\n')

    # clear the data in course data file
    def clear_course_data(self):
        with open(course_data_path, 'w') as file:
            file.write('')

    # return a number list which is generated based on the given current page number and total pages number
    def generate_page_num_list(self, page, total_pages):
        # according to the current page number
        # generate different list seperately
        if page <= 5:
            return [i for i in range(1, 10)]
        elif page > 5 and page < total_pages - 4:
            return [i for i in range(page - 4, page + 5)]
        elif page >= total_pages - 4:
            return [i for i in range(total_pages - 8, total_pages + 1)]

    # return a list of course objects
    # and the total pages number of courses and the total number of courses
    def get_courses_by_page(self, page):
        # load data from course data file
        course_list = []
        with open(course_data_path) as file:
            for line in file:
                line = line.strip('\n')
                line = line.split(';;;')
                # convert course information to course objects
                course_list.append(Course(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]))

        # to get the correct number of courses per page, the total page number, and the total number of courses
        if page * 20 > len(course_list):
            return (course_list[(page - 1) * 20:], ceil(len(course_list)/20), len(course_list))
        else:
            return (course_list[(page - 1) * 20: page * 20], ceil(len(course_list)/20), len(course_list))

    # return True if the delete of a specific course based on the course id is successful, otherwise return False
    # the course id in the instructor information should also be deleted
    def delete_course_by_id(self, temp_course_id):
        result = False
        # load data from course data file
        with open(course_data_path, 'r') as file:
            content = file.readlines()
        # rewrite the course data file
        with open(course_data_path, 'w') as file2:
            for line in content:
                temp_line = line.strip('\n').split(';;;')
                # skip the line which is the course id we want to delete
                if int(temp_line[5]) == temp_course_id:
                    result = True
                    continue
                file2.write(line)

        # load data from user data file
        with open(user_data_path, 'r') as file3:
            content2 = file3.readlines()
        # rewrite the user data file
        with open(user_data_path, 'w') as file4:
            for line in content2:
                temp_line = line.strip('\n').split(';;;')
                # find the line which contains the course id we want to delete
                if str(temp_course_id) in temp_line[-1].split('-'):
                    # delete the course id from the instructor information
                    temp_line[-1] = temp_line[-1].split('-')
                    temp_line[-1].remove(str(temp_course_id))
                    temp_line[-1] = '-'.join(temp_line[-1])
                    file4.write(';;;'.join([str(i) for i in temp_line]) + '\n')
                    continue
                # write down all other lines
                file4.write(line)
        return result

    # return a Course object based on the course id
    def get_course_by_course_id(self, temp_course_id):
        # load data from course data file
        course_list = []
        with open(course_data_path) as file:
            for line in file:
                course_list.append(line.strip('\n').split(';;;'))

        # find the line which contains the course id we want to get
        for course in course_list:
            if int(course[5]) == temp_course_id:
                # generate the comment based on other information in the course information
                if int(course[8]) > 100000 and float(course[9]) >= 4.5 and int(course[10]) >= 10000:
                    comment = 'Top Courses'
                elif int(course[8]) > 50000 and float(course[9]) >= 4.0 and int(course[10]) >= 5000:
                    comment = 'Popular Courses'
                elif int(course[8]) > 10000 and float(course[9]) >= 3.5 and int(course[10]) >= 1000:
                    comment = 'Good Courses'
                else:
                    comment = 'General Courses'
                return (Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6], course[7], course[8], course[9], course[10]), comment)

    # return a list of Course objects based on the instructor id and the total number of courses
    def get_course_by_instructor_id(self, instructor_id):
        # load data from course data file
        with open(user_data_path) as file:
            for line in file:
                line = line.strip('\n').split(';;;')
                # find the line which contains the instructor id we want to get
                if int(line[0]) == instructor_id and line[4] == 'instructor':
                    # get course ids in the instructor information
                    course_list = []
                    target_courses = line[-1].split('-')
                    # generate course objects based on the course ids obtained above
                    for course_id in target_courses:
                        course_list.append(self.get_course_by_course_id(int(course_id)))

                    # return the course objects and the total number of courses based on the number limitation
                    if len(course_list) > 20:
                        return (course_list[:20], len(course_list))
                    else:
                        return (course_list, len(course_list))

    # Generate a graph to show the top 10 subcategories with the most subscribers with a barplot.
    def generate_course_figure1(self):
        # load data from course data file
        with open(course_data_path, 'r') as file:
            course_list = []
            for line in file:
                line = line.strip().split(';;;')
                course_list.append(line)

        # extract required information and integrate them into a dataframe
        subcategory_list = [unit[2] for unit in course_list]
        num_subscribers_list = [int(unit[-3]) for unit in course_list]
        fig1_df = pd.DataFrame({'subcategory': subcategory_list, 'num_subscribers': num_subscribers_list})

        # process the dataframe to get the top 10 subcategories with the most subscribers
        figure_df = pd.DataFrame(fig1_df.groupby('subcategory')['num_subscribers'].sum())
        figure_df.reset_index(inplace=True)
        figure_df = figure_df.sort_values(by='num_subscribers', ascending=False).head(10)
        figure_df['subcategory'] = figure_df['subcategory'].apply(lambda x: ' '.join(x.split()[:3]))

        # generate the figure
        fig, ax = plt.subplots(figsize=(15, 10))

        plot1 = ax.bar(figure_df['subcategory'], figure_df['num_subscribers'])
        ax.set_xlabel('Subcategory', )
        ax.set_ylabel('Number of Subscribers')
        ax.set_title('Top 10 Subcategories with most subscribers')
        for label in ax.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        ax.bar_label(plot1, padding=3)
        plt.savefig(figure_save_path + 'course_figure1.png')

        return 'The subcategory with the most subcribers is Web Development. From the figure, we can see that the audiences are more insterested in programming.'
    
    # Generate a graph to show the top 10 courses that have lowest avg rating and over 50000 reviews with a barplot.
    def generate_course_figure2(self):
        # load data from course data file
        with open(course_data_path, 'r') as file:
            course_list = []
            for line in file:
                line = line.strip().split(';;;')
                course_list.append(line)

        # extract required information and integrate them into a dataframe
        course_titles = [course[6] for course in course_list if int(course[10]) > 50000]
        avg_ratings = [float(course[9]) for course in course_list if int(course[10]) > 50000]
        fig2_df = pd.DataFrame({'course_titles':course_titles, 'avg_ratings':avg_ratings})

        # process the dataframe to get the top 10 courses that have lowest avg rating and over 50000 reviews
        fig2_df_less = fig2_df.sort_values(by='avg_ratings').head(10)
        fig2_df_less['course_titles'] = fig2_df_less['course_titles'].apply(lambda x: ' '.join(x.split()[:3]))

        # generate the figure
        fig, ax2 = plt.subplots(figsize=(15, 10))

        plot1 = ax2.bar(fig2_df_less['course_titles'], fig2_df_less['avg_ratings'])
        ax2.set_xlabel('Courses', )
        ax2.set_ylabel('Average Rating')
        ax2.set_title('Top 10 Courses with lowest avrerage rating')
        for label in ax2.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        ax2.bar_label(plot1, padding=3)
        plt.savefig(figure_save_path + 'course_figure2.png')

        return 'The lowest average rating is 3.5. From the figure, we can see that lower ratings are around 4.5.'

    # Generate a graph to show the all the courses avg rating distribution that has subscribers between 100000 and 10000 with a scatterplot.
    def generate_course_figure3(self):
        # load data from course data file
        with open(course_data_path, 'r') as file:
            course_list = []
            for line in file:
                line = line.strip().split(';;;')
                course_list.append(line)

        # extract required information and integrate them into a dataframe
        avg_ratings = [float(course[9]) for course in course_list if int(course[8]) > 10000 and int(course[8]) < 100000]
        num_of_subscribers = [int(course[8]) for course in course_list if int(course[8]) > 10000 and int(course[8]) < 100000]
        fig3_df = pd.DataFrame({'avg_ratings': avg_ratings, 'num_of_subscribers':num_of_subscribers})

        # generate the figure
        fig, ax3 = plt.subplots(figsize=(15, 10))

        ax3.scatter(fig3_df['num_of_subscribers'], fig3_df['avg_ratings'])
        ax3.set_xlabel('Number of Subscribers')
        ax3.set_ylabel('Average Rating')
        ax3.set_title('Courses Average Rating Distribution among Subscribers between 100000 and 10000')
        plt.savefig(figure_save_path + 'course_figure3.png')

        return 'From the figure, we can see that there is no obvious relationship between average rating and number of subscribers. High average rating may have low subscribers.'

    # Generate a graph to show the number of courses for all categories and sort in ascending order with a piechart.
    def generate_course_figure4(self):
        with open(course_data_path, 'r') as file:
            course_list = []
            for line in file:
                line = line.strip().split(';;;')
                course_list.append(line)

        category_titles = [course[0] for course in course_list]
        course_ids = [course[5] for course in course_list]
        fig4_df = pd.DataFrame({'category_titles': category_titles, 'course_ids': course_ids})

        fig4_df = fig4_df.groupby(['category_titles']).agg({'course_ids': 'count'})
        fig4_df.reset_index(inplace=True)
        fig4_df = fig4_df.sort_values(by='course_ids')

        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.8, len(fig4_df)))


        fig, ax4 = plt.subplots(figsize=(10, 10))
        patches, texts, pcts = ax4.pie(fig4_df['course_ids'], colors=colors, autopct='%.2f%%',
                wedgeprops={'linewidth':2, 'edgecolor':'white'}, frame=False, labels=fig4_df['category_titles'],
                textprops={'size':'x-large'},
                explode=(0, 0, 0.1, 0))

        plt.setp(pcts, color='white')
        ax4.set_title('Number of Courses for All Categories', fontsize=18)
        plt.savefig(figure_save_path + 'course_figure4.png')

        return 'From the figure, we can see that the highest number of courses are in the category of Business. But the second large category, Development, is not that different from the first one.'

    # Generate a graph to show how many courses have reviews and how many courses do not have reviews with a barplot.
    def generate_course_figure5(self):
        # load data from course data file
        with open(course_data_path, 'r') as file:
            course_list = []
            for line in file:
                line = line.strip().split(';;;')
                course_list.append(line)

        # extract required information and integrate them into a dataframe
        num_of_no_reviews = len([course for course in course_list if int(course[10]) == 0])
        num_of_with_reviews = len(course_list) - num_of_no_reviews
        fig5_df = pd.DataFrame({'kind': ('with reviews', 'no reviews'), 'number': (num_of_with_reviews, num_of_no_reviews)})

        # generate the figure
        fig, ax5 = plt.subplots(figsize=(15, 10))

        plot1 = ax5.bar(fig5_df['kind'], fig5_df['number'])
        ax5.set_xlabel('Type of Courses', )
        ax5.set_ylabel('Number of Courses')
        ax5.set_title('Number of Courses with/without Reviews')
        for label in ax5.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        ax5.bar_label(plot1, padding=3)
        plt.savefig(figure_save_path + 'course_figure5.png')

        return 'From the figure, we can see that there are much more courses with reviews than there are courses without reviews.'

    # Generate a graph to show the top 10 subcategories with the least courses with a barplot.
    def generate_course_figure6(self):
        # load data from course data file
        with open(course_data_path, 'r') as file:
            course_list = []
            for line in file:
                line = line.strip().split(';;;')
                course_list.append(line)

        # extract required information and integrate them into a dataframe
        subcategory_list = [unit[2] for unit in course_list]
        course_ids = [unit[5] for unit in course_list]
        fig6_df = pd.DataFrame({'subcategory': subcategory_list, 'course_ids': course_ids})

        # process the dataframe to get the top 10 subcategories with the least courses
        figure_df = pd.DataFrame(fig6_df.groupby('subcategory')['course_ids'].count())
        figure_df.reset_index(inplace=True)
        figure_df = figure_df.sort_values(by='course_ids').head(10)
        figure_df['subcategory'] = figure_df['subcategory'].apply(lambda x: ' '.join(x.split()[:3]))

        # generate the figure
        fig, ax6 = plt.subplots(figsize=(15, 10))

        plot1 = ax6.bar(figure_df['subcategory'], figure_df['course_ids'])
        ax6.set_xlabel('Subcategory', )
        ax6.set_ylabel('Number of Courses')
        ax6.set_title('Top 10 Subcategories with Least Courses')
        for label in ax6.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        ax6.bar_label(plot1, padding=3)
        plt.savefig(figure_save_path + 'course_figure6.png')
        
        return 'From the figure we can see that the subcategory with least courses is IT Certifications.'