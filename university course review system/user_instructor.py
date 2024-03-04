"""
name : JUNTAO YU
student ID : 30358809 
start date : May 29th 2022
last modified date : June 10th 2022
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from math import ceil
from model.user import User
from lib.helper import user_data_path, course_json_files_path, figure_save_path

class Instructor(User):
    """
    Description: This class is used to get instrutor information and manipulate with it.
    And it is heritance from User class.
    """
    # constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",
    role="instructor", email="", display_name="", job_title="", course_id_list=[]):
        User.__init__(self, uid, username, password, register_time, role)
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    # reload print function
    def __str__(self):
        if self.display_name == "" and self.job_title == "" and self.course_id_list==[]:
            return f"{self.uid};;;{self.username};;;{self.encrypt_password(self.password)};;;{self.register_time};;;{self.role};;;{self.email};;;;;;;;;"
        else:
            return f"{self.uid};;;{self.username};;;{self.encrypt_password(self.password)};;;{self.register_time};;;{self.role};;;{self.email};;;{self.display_name};;;{self.job_title};;;{'-'.join(self.course_id_list)}"

    # this function is to extract instructor information from given json files
    def get_instructors(self):
        # load origin user txt to get exsited users
        # seperate instructors and other users for further process
        users = []
        instructors = []
        with open(user_data_path) as file:
            for line in file:
                line = line.strip().split(';;;')
                if line[4] != 'instructor':
                    users.append(line)
                else:
                    instructors.append(line)
        
        # convert instructors to dictionary
        instructor_dict = {}
        for instructor in instructors:
            instructor[-1] = instructor[-1].split('-')
            instructor_dict[int(instructor[0])] = instructor[1:]

        # read json files with multiple loops from course_json_files_path
        # course_json_files_path is a nested folder directory
        for path in os.listdir('.' + course_json_files_path):
            # the files in the folder are not all valid json files
            # filter out the invalid files
            if not path.startswith('.'):
                for category in os.listdir('.' + course_json_files_path + '/' + path):
                    if not category.startswith('.'):
                        for subcategory in os.listdir('.' + course_json_files_path + '/' + path + '/' + category):
                            with open('.' + course_json_files_path + '/' + path + '/' + category + '/' + subcategory, 'r') as f:
                                # load json file with json library
                                data = json.load(f)
                                # get instructor id from json file through key value pairs
                                for unit in data.values():
                                    # get all courses
                                    for items in unit['items']:
                                        # get instructors information from visible_instructors
                                        for instructor in items['visible_instructors']:
                                            # to check if the instructor is exsited in the dictionary
                                            # if not, add it to the dictionary, and add the course id as a list
                                            if instructor['id'] not in instructor_dict:
                                                instructor_id = instructor['id']
                                                username = instructor['display_name'].lower().replace(' ', '_')
                                                password = self.encrypt_password(str(instructor_id))
                                                register_time = 'yyyy-MM-dd_HH:mm:ss.SSS'
                                                email = username + '@gmail.com'
                                                role = 'instructor'
                                                displayname = instructor['display_name']
                                                job_title = instructor['job_title']
                                                course_id = [items['id']]
                                                instructor_dict[instructor_id] = [username, password, register_time, 
                                                role, email, displayname, job_title, course_id]
                                            # if the instructor is exsited in the dictionary, add the course id to the course id list
                                            else:
                                                if items['id'] not in instructor_dict[instructor['id']][-1]:
                                                 instructor_dict[instructor['id']][-1].append(items['id'])
        
        # write the user information back to user.txt
        with open(user_data_path, 'w') as file2:
            # write instructors first
            for k, v in instructor_dict.items():
                # convert the data in correct format before writing
                v[-1] = '-'.join([str(unit) for unit in v[-1]])
                instructor_info = str(k) + ';;;' + ';;;'.join([i if i != None else 'null' for i in v])
                file2.write(instructor_info + '\n')
            # write down other users
            for line in users:
                file2.write(';;;'.join(line) + '\n')

    # return a list of instructors based on the input page number
    # and the total number of pages, and the total number of instructors
    def get_instructors_by_page(self, page):
        # load user data and filter out only instructors
        instructor_list = []
        with open(user_data_path) as file:
            for line in file:
                line = line.strip().split(';;;')
                # convert instructor data to instructor object
                if line[4] == 'instructor':
                    line[-1] = line[-1].split('-')
                    instructor_list.append(Instructor(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8]))

        # to get the correct number of instructors per page, the total page number, and the total number of instructors
        if page * 20 > len(instructor_list):
            return (instructor_list[(page-1)*20:], ceil(len(instructor_list)/20), len(instructor_list))
        else:
            return (instructor_list[(page-1)*20:page*20], ceil(len(instructor_list)/20), len(instructor_list))

    # Generate a graph that shows the top 10 instructors who teach the most courses with a barchart.
    def generate_instructor_figure1(self):
        # load user data and filter out only instructors
        instructor_list = []
        with open(user_data_path) as file:
            for line in file:
                if line.strip().split(';;;')[4] == 'instructor':
                    line = line.strip().split(';;;')
                    line[-1] = line[-1].split('-')
                    instructor_list.append(line)

        # get required data from instructor_list
        insInfo_dict = {}
        insInfo_dict['displayname'] = [line[6] for line in instructor_list]
        insInfo_dict['no_of_courses'] = [len(line[-1]) for line in instructor_list]

        # integrate the data into a dataframe and sort it by the number of courses
        instructor_df = pd.DataFrame(insInfo_dict)
        instructor_df = instructor_df.sort_values(by='no_of_courses', ascending=False)
        instructor_top10 = instructor_df.head(10)

        x = instructor_top10['displayname']
        y = instructor_top10['no_of_courses']

        # generate the figure
        fig, ax7 = plt.subplots(figsize=(15, 10))

        plot1 = ax7.bar(x, y)
        ax7.set_xlabel('Number of courses')
        ax7.set_ylabel('Instructor')
        ax7.set_title('Top 10 Instructors with most courses')
        ax7.bar_label(plot1, padding=3)
        plt.savefig(figure_save_path + 'instructor_figure1.png')

        explaination = 'The highest number of courses is 30, and from the above graph, we can see that most of the top instructors teach 20 courses or more.'
        return explaination
