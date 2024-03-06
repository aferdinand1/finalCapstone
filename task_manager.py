# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("\nWrong password")
        continue
    else:
        print("\nLogin Successful!")
        logged_in = True

# Defining the functions for the menu.
def reg_user(menu):
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ").lower()

    # Loop for checking if username is in text file
    with open('user.txt', 'r') as file:
        # List for existing usernames
        existing_usernames = []
        for lines in file:
            login_details = lines.split(";")
            existing_usernames.append(login_details[0])
        # Loop for adding a unique username
        while new_username in existing_usernames:
            print("\nThis username already exists.")
            new_username = input("\nNew Username: ").lower()
            

    # - Request input of a new password
    new_password = input("New Password: ").lower()

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ").lower()

    # Loop for matching passwords
    while new_password != confirm_password:
        print("\nThe passwords do not match.")
        new_password = input("\nNew Password: ").lower()
        confirm_password = input("Confirm Password: ").lower()

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("\nNew user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    
    

def add_task(menu):
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
        }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all(menu):
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(menu):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    # User task number variable
    task_number = 0
    # Counter for number of user tasks
    task_number_counter = []
    for t in task_list:
        if t['username'] == curr_user:
            task_number += 1
            disp_str = f"Task {task_number}: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task completion: {t['completed']}\n"
            # Add task number to the counter
            task_number_counter.append(task_number)
            print(disp_str)
            
    # Ask if user would like to edit the tasks
    task_select_option = input("Would you like to select a task? (y/n): ").lower()
    while task_select_option not in ["n", "y"]:
        print("\nPlease select y or n.")
        task_select_option = input("\nWould you like to select a task? (y/n): ").lower()
    
    if task_select_option == "y":
        task_select()
    elif task_select_option == "n":
        print("\nYou will now return to the main menu.")
    

# Function for getting number of user tasks
def task_number_counter():
    task_number = 0 
    task_number_count = []
    for t in task_list:
        if t['username'] == curr_user:
            task_number += 1
            task_number_count.append(task_number)
    return task_number_count
    
# Function for totalling the number of user tasks
def task_number_totaller():
    task_number = 0
    for t in task_list:
        if t['username'] == curr_user:
            task_number += 1
    return task_number
    
# Function to select a task 
def task_select():
    # Number of tasks the user has in total
    task_number_count = task_number_counter()
    # Number of tasks the user has in a list form
    task_number_total = task_number_totaller()
    # User menu with functions
    task_option = input("\nPlease select a task (type -1 to exit): ")
    # For checking task option is valid
    task_option_boolean = False
    # Check if the user entered an integer or not
    while task_option_boolean is False:
        try:
            task_option = int(task_option)
        except:
            print("\nYou have not entered a number. Please try again.")
            task_option = input("\nPlease select a task (type -1 to exit): ")
    # If integer, check if option typed is a valid task
        else:
            if int(task_option) == -1:
                task_option_boolean = True
                print("\nYou will now return to the main menu.")
            elif int(task_option) == 0:
                print("\nThis is not an option. Please try again.")
                task_option = input("\nPlease select a task (type -1 to exit): ")
            elif int(task_option) not in task_number_count:
                print(f"\nThere is no task {task_option} for this user. Please try again.")
                task_option = input("\nPlease select a task (type -1 to exit): ")
            # If a valid task, enable to be edited.
            elif int(task_option) in task_number_count:
                task_option_boolean = True
                print(f"\nYou have selected task number {task_option}.\n")
                # Get a list of user tasks and the components of the selected task
                user_tasks = get_user_tasks()
                user_task = str(user_tasks[task_option])
                user_task_parts = user_task.split(',')
                user_task_dict = {}
                user_task_counter = 0
                # Loop to convert user task (list) into dictionary and print out the task
                for i in range (0, len(user_task_parts)):
                    user_task_dict[user_task_counter] = user_task_parts[user_task_counter]
                    print(user_task_parts[int(user_task_counter)])
                    user_task_counter += 1
                # Add the option to edit the task or mark as complete
                task_select_option = input("Would you like to mark the task as complete (c) or edit the task (e) (press -1 to exit)?: ").lower()
                task_select_option_boolean = False
                while task_select_option_boolean is False:
                    if task_select_option == "e":
                        task_select_option_boolean = True
                        task_edit(task_option)
                    elif task_select_option == "c":
                        task_select_option_boolean = True
                        mark_complete(task_option)
                    elif task_select_option == "-1":
                        print("\nYou will now return to the main menu.")
                        task_select_option_boolean = True
                    else:
                        print("\nYou have selected an incorrect option. Please try again.")
                        task_select_option = input("\nWould you like to mark the task as complete (c) or edit the task (e)?: ").lower()


# Function for editing a task
def task_edit(task_option):
    task_number = 0
    selected_task_number_counter = 0
    for t in task_list:
        selected_task_number_counter += 1
        if t['username'] == curr_user:
            task_number += 1
            if task_number == task_option:
                selected_task_number_counter -= 1
                selected_task_number = selected_task_number_counter
                selected_task = task_data[selected_task_number_counter]
    selected_task = selected_task.split(";")
    if selected_task[5] == "Yes":
        print("\nThis task has been marked as complete and cannot be edited.")
    else:
        edit_choice_boolean = False
        edit_choice = input("\nWould you like to edit the asigned username (u) or the due date (d) (press -1 to exit)?: ").lower()
        while edit_choice_boolean is False:
            if edit_choice == "u":
                edit_choice_boolean = True
                new_username_boolean = False
                new_username = input("\nPlease enter the user name you would like to assign the task to: ")
                while new_username_boolean is False:
                    # To check if username exists
                    new_username_check = False
                    with open('user.txt', 'r') as file:
                        # List for existing usernames
                        existing_usernames = []
                        for lines in file:
                            login_details = lines.split(";")
                            existing_usernames.append(login_details[0])
                        if new_username in existing_usernames:
                            new_username_boolean = True
                            new_username_check = True
                        else: 
                            print("\nThis user name does not exist.")
                            new_username = input("\nPlease enter the user name you would like to assign the task to: ")
                # Change the username for the task and write to text file
                if new_username_check == True:
                    selected_task[0] = new_username
                    selected_task = (";").join(selected_task)
                    task_data[selected_task_number] = selected_task
                    task_data_update = ("\n").join(task_data)
                    with open('tasks.txt', 'w') as file:
                        file.write(task_data_update)
                    print("\nThe username has been updated.")
            elif edit_choice == "d":
                edit_choice_boolean = True
                # Check if date time entered follows the format
                while True:
                    try:
                        new_date = input("\nEnter the new date (YYYY-MM-DD): ")
                        new_date_string = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                        break
                    except ValueError:
                        print("\nInvalid datetime format. Please use the format specified.")
                selected_task[3] = new_date_string.strftime(DATETIME_STRING_FORMAT)
                selected_task = (";").join(selected_task)
                task_data[selected_task_number] = selected_task
                task_data_update = ("\n").join(task_data)
                with open('tasks.txt', 'w') as file:
                    file.write(task_data_update)
                print("\nThe due date has now been updated.")
            elif edit_choice == "-1":
                edit_choice_boolean = True
                print("You will now be returned to the main menu.")
            else:
                print("\nYou have entered an incorrect option. Please try again.")
                edit_choice = input("\nWould you like to edit the asigned username (u) or the due date (d)?: ").lower()
    

# Function for marking user task as complete
def mark_complete(task_option):
    selected_task_number = 0
    task_number = 0
    for t in task_list:
        selected_task_number += 1
        if t['username'] == curr_user:
            task_number += 1
            if task_number == task_option:
                selected_task_number -= 1
                selected_task = task_data[selected_task_number]
                selected_task = selected_task.split(";")
                for i in range(0, len(selected_task)):
                    if selected_task[i] == "Yes" or selected_task[i] == "No":
                        selected_task[i] = "Yes"
                        selected_task = (";").join(selected_task)
                        task_data[selected_task_number] = selected_task
    task_data_update = ("\n").join(task_data)
    with open('tasks.txt', 'w') as file:
        file.write(task_data_update)
    print("\nYour task has now been marked as complete.")
    
# Function for getting a list of user tasks.
def get_user_tasks():
    task_number = 0
    user_tasks = {}
    for t in task_list:
        if t['username'] == curr_user:
            task_number += 1
            disp_str = f"Task {task_number}: {t['title']},"
            disp_str += f"Assigned to: {t['username']},"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)},"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)},"
            disp_str += f"Task Description: {t['description']},"
            disp_str += f"Task completion: {t['completed']},"
            user_tasks[task_number] = disp_str
    return user_tasks

# Function for generating reports
def generate_report():
    task_overview()
    user_overview()
    print()
    print("task_overview.txt has now been updated.")
    print("User_overview.txt has now been updated.")

def task_overview():
    # Total number of tasks
    total_tasks = 0
    for t in task_list:
        total_tasks += 1
    # Total completed tasks
    completed_tasks = 0
    for t in task_list:
        if t['completed'] is True:
            completed_tasks += 1
    # Total uncompleted tasks
    uncompleted_tasks = 0
    for t in task_list:
        if t['completed'] is False:
            uncompleted_tasks += 1
    # Uncompleted tasks that are overdue
    today = date.today()
    overdue_tasks = 0
    for t in task_list:
        if t['completed'] == False:
            if datetime.date(t['due_date']) < today:
                overdue_tasks += 1
    # Percentage of tasks that are incomplete
    incomplete_task_percentage = f"{uncompleted_tasks / total_tasks * 100}%"
    # Percentage of tasks that are overdue
    overdue_task_percentage = f"{overdue_tasks / total_tasks * 100}%"

    file_update = f'''Task overview
        
The total number of tasks that have been generated and tracked: {total_tasks}

The total number of completed tasks: {completed_tasks}

The total number of uncompleted tasks: {uncompleted_tasks}

The total number of tasks that haven't been completed and are overdue: {overdue_tasks}

The percentage of tasks that are incomplete: {incomplete_task_percentage}

The percentage of tasks that are overdue: {overdue_task_percentage}
'''
    with open('task_overview.txt', 'w') as file:
        file.write(file_update)

    
    
# Function for generating user_overview report file
def user_overview():
    # Total number of users registered
    user_number = 0
    for u in user_data:
        user_number += 1
    # Total number of tasks
    total_tasks = 0
    for t in task_list:
        total_tasks += 1
    # List of users
    users = []
    for u in user_data:
        login_details = u.split(";")
        users.append(login_details[0])
    # For each user
    # Total number of tasks assigned to each user.
    user_task_numbers = {}
    for u in users:
        user_task_number = 0
        for t in task_list:
            if u == t['username']:
                user_task_number += 1
        user_task_numbers[u] = user_task_number
    # The percentage of the total number of tasks assigned to that user
    user_task_percentages = {}
    for u in users:
        user_task_percentages[u] = f"{user_task_numbers[u] / total_tasks * 100}%"
    # Percentage of tasks assigned to user that have been completed
    user_completed_tasks = {}
    user_completed_tasks_percentage = {}
    for u in users:
        completed_tasks = 0
        for t in task_list:
            if t['username'] == u:
                if t['completed'] == True:
                    completed_tasks += 1
        user_completed_tasks[u] = completed_tasks
    for u in users:
        if user_task_numbers[u] != 0:
            user_completed_tasks_percentage[u] = f"{user_completed_tasks[u] / user_task_numbers[u] * 100}%"
        else:
            user_completed_tasks_percentage[u] = f"{0}%"
    # Percentage of tasks that must still be completed
    user_incomplete_tasks = {}
    user_incomplete_tasks_percentage = {}
    for u in users:
        incomplete_tasks = 0
        for t in task_list:
            if t['username'] == u:
                if t['completed'] == False:
                    incomplete_tasks += 1
        user_incomplete_tasks[u] = incomplete_tasks
    for u in users:
        if user_task_numbers[u] != 0:
            user_incomplete_tasks_percentage[u] = f"{user_incomplete_tasks[u] / user_task_numbers[u] * 100}%"
        else:
            user_incomplete_tasks_percentage[u] = f"{0}%"
    # Percentage of tasks that are not completed and overdue
    user_overdue_tasks = {}
    user_overdue_tasks_percentages = {}
    today = date.today()
    for u in users:
        overdue_tasks = 0
        for t in task_list:
            if t['username'] == u:
                if datetime.date(t['due_date']) < today:
                    overdue_tasks += 1
        user_overdue_tasks[u] = overdue_tasks
    for u in users:
        if user_task_numbers[u] != 0:
            user_overdue_tasks_percentages[u] = f"{user_overdue_tasks[u] / user_task_numbers[u] * 100}%"
        else:
            user_overdue_tasks_percentages[u] = f"{0}%"
    # Formatting each variable for updating the file
    user_task_numbers_list = []
    for u in users:
        user_task_numbers_list.append(f"{u}: {user_task_numbers[u]}")
    user_task_numbers_formatted = ("\n").join(user_task_numbers_list)

    user_task_percentages_list = []
    for u in users:
        user_task_percentages_list.append(f"{u}: {user_task_percentages[u]}")
    user_task_percentages_formatted = ("\n").join(user_task_percentages_list)
    
    user_completed_tasks_percentage_list = []
    for u in users:
        user_completed_tasks_percentage_list.append(f"{u}: {user_completed_tasks_percentage[u]}")
    user_completed_tasks_percentage_formatted = ("\n").join(user_completed_tasks_percentage_list)
    
    user_incomplete_tasks_percentage_list = []
    for u in users:
        user_incomplete_tasks_percentage_list.append(f"{u}: {user_incomplete_tasks_percentage[u]}")
    user_incomplete_tasks_percentage_formatted = ("\n").join(user_incomplete_tasks_percentage_list)
    
    user_overdue_tasks_percentages_list = []
    for u in users:
        user_overdue_tasks_percentages_list.append(f"{u}: {user_overdue_tasks_percentages[u]}")
    user_overdue_tasks_percentages_formatted = ("\n").join(user_overdue_tasks_percentages_list)

    file_update = f'''User overview

The total number of users registered: {user_number}

The total number of tasks that have been generated and tracked: {total_tasks}

Task data for each user:

Total number of tasks assigned to each user:

{user_task_numbers_formatted}

The percentage of the total number of tasks that have been assigned to each user: 

{user_task_percentages_formatted}

The percentage of tasks assigned to each user that have been completed: 

{user_completed_tasks_percentage_formatted}

The percentage of tasks assigned to each user that must still be completed: 

{user_incomplete_tasks_percentage_formatted}

The percentage of tasks assigned to each user that have not yet been completed and are overdue: 

{user_overdue_tasks_percentages_formatted}
'''
    with open('user_overview.txt', 'w') as file:
        file.write(file_update)

def display_statistics():
    '''If the user is an admin they can display statistics about number of users
            and tasks.'''
    # Modified function that gathers this data from the text files
    num_users = 0
    num_tasks = 0

    # Code to generate files if not already on the system
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            pass

    # Get number of users from txt file
    with open('user.txt', 'r') as file:
        user_strings = file.read().split("\n")
    
    num_users = 0
    for u in user_strings:
        num_users += 1

    # Get number of tasks from text file
    with open('tasks.txt', 'r') as file:
        task_strings = file.read().split("\n")
    
    num_tasks = 0
    for t in task_strings:
        num_tasks += 1

    # Display statistics
    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")  
    
while True:
    # If current user is admin the menu will be different
    if curr_user == "admin":
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    else:
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    ds - Display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':
      reg_user(menu)

    elif menu == 'a':
       add_task(menu)

    elif menu == 'va':
       view_all(menu)

    elif menu == 'vm':
        view_mine(menu)
    
    elif menu == 'gr':
        generate_report()
                
    elif menu == 'ds' and curr_user == 'admin': 
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
