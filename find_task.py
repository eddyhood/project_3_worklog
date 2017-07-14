import collections
import csv
import datetime
import logging
import os
import re

import add_task
import work_log
import utils

# Set up custom logger for the module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logs/find_tasks.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


def search_options():
    """Displays the different search options for existing tasks"""
    utils.clear_screen()
    print("""Choose a search method:\n
          [A] Date Range\n
          [B] Logs by Date\n
          [C] Time spent\n
          [D] Exact (Phrase) search\n
          [E] Regex Pattern\n
          [F] Return to main menu\n
          [G] Quit the program
          """)
    choose_search = input("Select an option: ")
    logger.info("User selected {} for a search method.".format(choose_search))
    search_choice(choose_search)


def search_choice(user_choice):
    """Launch search method based on user's choice"""
    try:
        if user_choice.upper() == "A":
            date_search()
        elif user_choice.upper() == "B":
            date_counter()
        elif user_choice.upper() == "C":
            time_search()
        elif user_choice.upper() == "D":
            exact_search()
        elif user_choice.upper() == "E":
            pattern_search()
        elif user_choice.upper() == "F":
            work_log.main_menu()
        elif user_choice.upper() == "G":
            utils.quit_program()
        else:
            raise ValueError
    except ValueError:
        logger.warning("Exception raised.  User typed {} for a search method."
                       .format(user_choice))
        print("\nYou entered an invalid option")
        repeat = input("Press 'any key' to try again or type QUIT to leave: ")
        if repeat.upper() == "QUIT":
            utils.clear_screen()
            utils.quit_program()
        else:
            utils.clear_screen()
            search_options()
        logger.info("User selected {} to fix search error.".format(repeat))


def date_search():
    """Seaches for past entries based on an exact date entered"""
    utils.clear_screen()
    print("==========  Find a Worklog Entry by Exact Date  ==========")
    while True:
        # Get date and make sure it's in correct format or throw error
        try:
            get_date = input("Enter a date as MM/DD/YYYY: ")
            datetime.datetime.strptime(str(get_date), "%m/%d/%Y")
        except ValueError:
            print("Please enter a valid date as MM/DD/YYYY")
        # Look for date in csv file and call failed search or success search
        else:
            result = []
            with open("tasklogs.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if re.search(get_date, row["Task Date"]):
                        result.append(row)
            if result == []:
                failed_search()
            else:
                success_search(result)


def date_counter():
    """Step#1 of date range serach: Open CSV file and count # of dates"""
    result = []
    with open("tasklogs.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row["Task Date"])
    csvfile.close()
    date_count = collections.Counter(result)
    logger.info("Results for date range include: {}".format(date_counter))
    date_lister(date_count)


def date_lister(date_count):
    """Step #2 of date range search: Show dates and total logs per date"""
    ordered_dict = collections.OrderedDict(sorted(date_count.items()))
    utils.clear_screen()
    print("=============  Date & Log Entries Include  =============\n")
    number = 0
    for date, count in ordered_dict.items():
        number += 1
        if count == 1:
            print("#{} - {} = {} log".format(number, date, count))
        else:
            print("#{} - {} = {} logs".format(number, date, count))
    date_chooser(ordered_dict)


def date_chooser(ordered_dict):
    """Step #3 of date range search: Let user choose a date to view"""
    while True:
        try:
            choose_date = int(input("\nEnter [#] to see logs for that date: "))
            logger.info("User entered {} to choose a date".format(choose_date))
        except ValueError:
            print("Error: i.e. Enter [1] for the first date in the list""")
        else:
            break
    get_index = choose_date - 1
    get_date = list(ordered_dict.keys())[get_index]
    logger.info("Chosen date is {}".format(get_date))
    display_logs(get_date)


def display_logs(get_date):
    """Step #4 of date range search: Display all logs for the chose date"""
    result = []
    with open("tasklogs.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if re.search(get_date, row["Task Date"]):
                result.append(row)
    if result == []:
        failed_search()
    else:
        success_search(result)


def time_search():
    """Searches for past entires based on amount of time logged"""
    utils.clear_screen()
    print("==========  Find a Worklog Entry by Time Spent  ==========")

    while True:
        try:
            search_term = input("Enter time. i.e. [50] for 50 minutes: ")
        except ValueError:
            print("Try again.  Remember, you can only enter numbers.")
        else:
            break
    result = []
    with open("tasklogs.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if re.search(search_term, row["Task Time"]):
                result.append(row)
    if result == []:
        failed_search()
    else:
        success_search(result)


def exact_search():
    """Searches for past entires based on exact match in name or notes"""
    utils.clear_screen()
    print("==========  Find a Worklog Entry by Exact Match  ==========")
    search_term = input("Enter a search term: ")
    result = []
    with open("tasklogs.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if re.search(search_term, row["Task Name"], re.I):
                result.append(row)
            elif re.search(search_term, row["Task Note"], re.I):
                result.append(row)
    if result == []:
        failed_search()
    else:
        success_search(result)


def pattern_search():
    """Searches for past entires based on an entered regex pattern"""
    utils.clear_screen()
    print("==========  Find a Worklog Entry by Pattern  ==========")
    try:
        result = []
        search_term = input("Enter a regular expression pattern: ")
        regex_pattern = re.compile(search_term, re.I)

        with open("tasklogs.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if regex_pattern.search(row["Task Name"]):
                    result.append(row)
                elif regex_pattern.search(row["Task Note"]):
                    result.append(row)
        if result == []:
            failed_search()
        else:
            success_search(result)
    except Exception as e:
        print(e)


def delete_row(row_to_del):
    filename = "tasklogs.csv"
    temp_file = "task_temp.csv"
    with open(filename) as csvin, open(temp_file, "w") as csvout:
        reader = csv.DictReader(csvin)
        fieldnames = ["Task Name", "Task Date", "Task Date DT",
                      "Task Time", "Task Note", "Task Timestamp"]
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row == row_to_del:
                break
            else:
                writer.writerow(row)
        writer.writerows(reader)
    os.remove(filename)
    os.rename(temp_file, filename)
    utils.clear_screen()
    print("=========  Log Has Been Deleted  =========\n\n")
    print("[M]ain Menu [A]dd log [S]earch log [Q]uit program\n")
    get_choice = input("Choose an option: ")
    if get_choice.upper() == "M":
        work_log.main_menu()
    elif get_choice.upper() == "A":
        add_task.Task()
    elif get_choice.upper() == "S":
        search_options()
    elif get_choice.upper() == "Q":
        utils.quit_program()


def success_search(result):
    """Shows all worklogs found & gives user ability to scroll through them"""
    utils.clear_screen()
    total_results = len(result)
    display_result(result[0])
    index = 0

    while True:
        try:
            # Show worklog results found in the format 1 of 2.
            if 0 <= index <= (total_results-1):
                position_index = index + 1
            elif index > total_results:
                position_index = total_results
            print("Result {} of {}".format(position_index, total_results))

            # Take user input to scroll through tasks or leave view
            choice = input("\n[N]ext [P]revious [E]dit [D]elete [M]ain Menu: ")
            if choice.upper() == "N":
                try:
                    utils.clear_screen()
                    index += 1
                    display_result(result[index])
                except IndexError:
                    print("There are no more worklogs to view.")
            elif choice.upper() == "P":
                if index == 0:
                    utils.clear_screen()
                    print("There are no more worklogs to view")
                else:
                    utils.clear_screen()
                    index -= 1
                    display_result(result[index])
            elif choice.upper() == "E":
                edit_log(result[index])
            elif choice.upper() == "D":
                delete_row(result[index])
            elif choice.upper() == "M":
                work_log.main_menu()
            else:
                raise ValueError
        except ValueError:
            utils.clear_screen()
            print("Please enter a valid option")


def display_result(row):
    """Generic function to display a task found in a search result"""
    print("""Successful Search! Here's what we found:\n
          Task Name: {}\n
          Task Date: {}\n
          Task Time: {}\n
          Task Note: {}\n
          """.format(row["Task Name"], row["Task Date"],
                     row["Task Time"], row["Task Note"]))


def failed_search():
    """Message & options that show when a search function comes up empty"""
    utils.clear_screen()
    print("Bummer! Your search did not return any queries.")
    print("What would you like to do next?")
    choice = input("[M]ain Menu [S]earch again [Q]uit: ")
    if choice.upper() == "M":
        work_log.main_menu()
    elif choice.upper() == "S":
        search_options()
    elif choice.upper() == "Q":
        utils.quit_program()


def edit_log(log_to_edit):
    """Allows user to edit a log entry"""
    utils.clear_screen()
    lookup = list(log_to_edit.values())
    logger.info("Lookup list = {}".format(lookup))

    # Present user with a menu of options for the edit
    print(""""You have chosen to edit the following tasK:\n
          [A] Task Name: {}\n
          [B] Task Date: {}\n
          [C] Task Time: {}\n
          [D] Task Note: {}\n
          """.format(lookup[0], lookup[1],
                     lookup[3], lookup[4]))

    # Get user's edit value
    get_choice = input("Enter an option to edit: ")
    try:
        if get_choice.upper() == "A":
            get_name = input("Enter a new task name: ")
            lookup[0] = get_name
        elif get_choice.upper() == "B":
            get_date = input("Enter a new task date as MM/DD/YYYY: ")
            lookup[1] = get_date
        elif get_choice.upper() == "C":
            get_time = int(input("Enter a new time: "))
            lookup[3] = get_time
        elif get_choice.upper() == "D":
            get_note = input("Enter a new task note: ")
            lookup[4] = get_note
        else:
            raise ValueError
    except ValueError:
        print("Whoops! Please enter a valid option to edit.")
    logger.info("After edits, log will be: {}".format(lookup))

    # Write user edit to log in csv file
    filename = "tasklogs.csv"
    temp_file = "task_temp.csv"
    with open(filename) as csvin, open(temp_file, "w") as csvout:
        reader = csv.DictReader(csvin)
        fieldnames = ["Task Name", "Task Date", "Task Date DT",
                      "Task Time", "Task Note", "Task Timestamp"]
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row["Task Timestamp"] == lookup[5]:
                writer.writerow({
                                "Task Name": lookup[0],
                                "Task Date": lookup[1],
                                "Task Time": lookup[3],
                                "Task Note": lookup[4]
                                })
                break
            else:
                writer.writerow(row)
        writer.writerows(reader)
    os.remove(filename)
    os.rename(temp_file, filename)
    display_edit(lookup)


def display_edit(lookup):
    """Shows congratulation message and edited log"""
    utils.clear_screen()
    print("=======  Congratulations! Your Log Was Edited  =======")
    print("You can review your changes below:")
    print("""
          Task Name: {}\n
          Task Date: {}\n
          Task Time: {}\n
          Task Note: {}\n
          """.format(lookup[0], lookup[1], lookup[3], lookup[4]))
    print("[A]dd Task [S]earch Task [M]ain Menu [Q]uit")
    get_choice = input("Choose an Option:")
    while True:
        try:
            if get_choice.upper() == "A":
                add_task.Task()
            elif get_choice.upper() == "S":
                search_options()
            elif get_choice.upper() == "M":
                work_log.main_menu()
            elif get_choice.upper() == "Q":
                utils.quit_program()
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid option")
