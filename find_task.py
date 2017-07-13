import logging
import re
import csv

import work_log
import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logs/find_tasks.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)

# When finding previous entry, they can: find by date, find by time spent,
# find by exact search, find by pattern

# When finding by date, present a list of dates with entries and be able
# to choose on to see entries from.

# When finding by time spent, user can enter the number of minutes a task took
# and be able to choose one to see entires from.

# When finding by exact string, user should be allowed to enter a string and
# then be presented with entries containing that string in the task name
# or notes.

# When finding by pattern, user should be allowed to enter a regular expression
# and then be presented with entries matching that pattern in their task
# name or notes.

# When displaying the entries, the entires should be in a readable format with
# the date, task name, time spent, and note info.


# Entries can be deleted and edited, letting user change the date, task name,
# time spent, and/or notes.

# Entries can be searched for and found based in a date range. For example,
# 01/01/2016 and 12/31/2016.

# Entries are displayed one at a time with the ability to page through
# records (previous,next/back).


def search_options():
    """Displays the different search options for existing tasks"""
    utils.clear_screen()
    print("""Choose a search method:\n
          [D] Find by date\n
          [T] Find by time spent\n
          [E] Find by exact search\n
          [P] Find by pattern\n
          [M] Return to main menu\n
          [Q] Quit the program
          """)
    choose_search = input("Select an option: ")
    logger.info("User selected {} for a search method.".format(choose_search))

    try:
        """Compares answer to options & throws an exception if non-existent"""
        if choose_search.upper() == "D":
            date_search()
        elif choose_search.upper() == "T":
            time_search()
        elif choose_search.upper() == "E":
            exact_search()
        elif choose_search.upper() == "P":
            pattern_search()
        elif choose_search.upper() == "M":
            work_log.main_menu()
        elif choose_search.upper() == "Q":
            utils.quit_program()
        else:
            raise ValueError
    except ValueError:
        logger.warning("Exception raised.  User typed {} for a search method."
                       .format(choose_search))
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
    """Seaches for past entries based on a date range"""
    utils.clear_screen()
    print("==========  Find a Worklog Entry by Date  ==========")

    while True:
        try:
            search_term = input("Enter a date to search by: ")
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
            choice = input("\n[N]ext [P]revious [S]earch [M]ain Menu [Q]uit ")
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
            elif choice.upper() == "S":
                search_options()
            elif choice.upper() == "M":
                work_log.main_menu()
            elif choice.upper() == "Q":
                utils.quit_program()
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
    choice = input("[M]ain Menu [S]earch again [Q]uit ")
    if choice.upper() == "M":
        work_log.main_menu()
    elif choice.upper() == "S":
        search_options()
    elif choice.upper() == "Q":
        utils.quit_program()
