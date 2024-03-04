from Admin import Admin
from User import User
from Student import Student
from Instructor import Instructor


def show_menu(user_object):
    """
    To print info to show the list

    This function shows the identity of the user and
    print out the functions they can approach

    Parameters
    ----------
    user_object : object
        keyword used to print related info

    Returns
    -------

    Examples
    --------

    """
    print(user_object.__class__.__name__ + ' login successfully\nWelcome ' + user_object.username + '. Your role is ' + user_object.__class__.__name__ + '.')
    print('Please enter ' + user_object.__class__.__name__ + ' command for further service:')
    print('1. EXTRACT_DATA\n2. VIEW_COURSES\n3. VIEW_USERS\n4. VIEW_REVIEWS\n5. REMOVE_DATA')


def process_operations(user_object):
    """
    To achieve functions provided to users

    This function call the function from different class to
    extract data,remove data. view different info based on
    user prompts.


    Parameters
    ----------
    user_object : object
        keyword used to match info

    Returns
    -------

    Examples
    --------

    """
    while True:
        command = input().split()
        if command[0] == '1':
            user_object.extract_info()
        elif command[0] == '2':
            if len(command) == 3:
                args = [command[1], command[2]]
                user_object.view_courses(args)
            else:
                user_object.view_courses()
        elif command[0] == '3':
            user_object.view_users()
        elif command[0] == '4':
            if len(command) == 3:
                args = [command[1], command[2]]
                user_object.view_reviews(args)
            else:
                user_object.view_reviews()
        elif command[0] == '5':
            user_object.remove_data()
        elif command[0] == 'logout':
            print('Thank you for using our system')
            main()
        elif command[0] == 'exit':
            print('Thank you for using our program')
            quit()


def main():
    """
    To identify the user and call proper function

    This function ask user to log in and call the function
    in user class. then based on the result call the proper function
    to achieve the goal of this program

    Parameters
    ----------

    Returns
    -------

    Examples
    --------

    """
    # have while loop to handle error
    while True:
        # get user input to have temp user info
        inp = input('Please input username and password to login:(format username password)\n').split()
        if inp[0] == 'exit':
            print('Thank you for using our program')
            quit()
        if len(inp) != 2:
            print('format incorrect')
        else:
            # call the user class to create user object the first attribute take -1 just to run login method. cuz id is not using here. login method would return the true id.
            temp_user = User(-1, inp[0], inp[1])
            # To check if the login succeeds.
            if temp_user.login()[0]:
                # To confirm the role in order to choose which class of object to create
                if temp_user.login()[1] == 'Admin':
                    # get info from login method returned data and create related object
                    user_object = Admin(temp_user.login()[2], temp_user.login()[3], temp_user.login()[4])
                    show_menu(user_object)
                    process_operations(user_object)
                elif temp_user.login()[1] == 'Student':
                    # get info from login method returned data and create related object
                    user_object = Student(temp_user.login()[2], temp_user.login()[3], temp_user.login()[4])
                    show_menu(user_object)
                    process_operations(user_object)
                elif temp_user.login()[1] == 'Instructor':
                    # get info from login method returned data and create related object
                    user_object = Instructor(temp_user.login()[2], temp_user.login()[3], temp_user.login()[4])
                    show_menu(user_object)
                    process_operations(user_object)
            else:
                print('username or password incorrect')


if __name__ == "__main__":
    # print a welcome message
    print('Welcome to our system')
    # manually register admin
    admin = Admin('-1', 'admin', 'admin')
    admin.register_admin()
    main()







