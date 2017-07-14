import logging

import add_task
import find_task
import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logs/work_log.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


def main_menu():
    """Displays the beginning main menu for the application"""
    utils.clear_screen()
    print("=============  Welcome to the Company Worklog!  =============\n")

    while True:
        try:
            # Present main menu to user
            print("\n[A]dd entry\n[S]earch logs\n[Q]uit\n\n")
            goal = input("Select an option: ")
            logger.info("User selected {} on main menu.".format(goal))

            # Compares answer to options and thows an exception if missing
            if goal.upper() == "A":
                add_task.Task()
            elif goal.upper() == "S":
                find_task.search_options()
            elif goal.upper() == "Q":
                utils.quit_program()
            else:
                raise Exception
        except Exception:
            utils.clear_screen()
            logger.warning("Exception raised.  User typed {}.".format(goal))
            print("\nWhoops, that didn't work. Please try again.\n")
        else:
            utils.clear_screen()
            break


if __name__ == "__main__":
    main_menu()
