import sys
import logging

import add_task
import find_task
import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logging_files/work_log.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


# Present a menu of options: Add new entry or look up previous entry

# Runs without error and all exceptions are caught in a meaningful way

# When entering a new work log, user enters: task name, date,
# number of minutes spent, and any additional notes they want to record.

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

# Menu must have a quit option to exit the program.

# Entries can be deleted and edited, letting user change the date, task name,
# time spent, and/or notes.

# Entries can be searched for and found based in a date range. For example,
# 01/01/2016 and 12/31/2016.

# Entries are displayed one at a time with the ability to page through
# records (previous,next/back).


def main_menu():
    """Displays the beginning main menu for the application"""
    utils.clear_screen()
    print("=============  Welcome to the Company Worklog!  =============\n")
    goal = input("""What would you like to do?\n
                 [A] Add a new entry\n
                 [S] Search for a previous entry?\n\n
                 Select an option: """)
    logger.info("User selected {} on main menu.".format(goal))
    try:
        """Compares answer to options and thows an exception if missing"""
        if goal.upper() == "A":
            add_task.Task()
        elif goal.upper() == "S":
            find_task.search_options()
        else:
            raise ValueError
    except ValueError:
        logger.warning("Exception raised.  User typed {}.".format(goal))
        print("\nYou must enter [A] or [S] as a selection.")
        repeat = input("Press 'any key' to try again or type QUIT to leave. ")
        if repeat == "":
            utils.clear_screen()
            main_menu()
        elif repeat.upper() == 'QUIT':
            utils.clear_screen()
            utils.quit_program()
        else:
            utils.clear_screen()
            main_menu()


if __name__ == "__main__":
    main_menu()
