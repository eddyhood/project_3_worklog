import sys

import work_log
from utils import clear_screen


def search_options():
    """Displays the different search options for existing tasks"""
    clear_screen()
    print("""Choose a search method:\n
          [A] Find by date\n
          [B] Find by time spent\n
          [C] Find by exact search\n
          [D] Find by pattern\n
          [E] Return to main menu\n
          """)
    choose_search = input("Select an option: ")

    try:
        """Compares answer to options & throws an exception if non-existent"""
        if choose_search.upper() == "A":
            date_search()
        elif choose_search.upper() == "B":
            time_search()
        elif choose_search.upper() == "C":
            exact_search()
        elif choose_search.upper() == "D":
            pattern_search()
        elif choose_search.upper() == "E":
            clear_screen()
            work_log.main_menu()
        else:
            raise ValueError
    except ValueError:
        print("\nYou entered an invalid option")
        repeat = input("Press 'any key' to try again or type QUIT to leave: ")
        if repeat == "":
            clear_screen()
            search_options()
        elif repeat.upper() == "QUIT":
            clear_screen()
            print("Thanks for visiting the worklog!")
            sys.exit()
        else:
            clear_screen()
            search_options()


def date_search():
    """Seaches for past entries based on a date range"""
    pass


def time_search():
    """Searches for past entires based on amount of time logged"""
    pass


def exact_search():
    """Searches for past entires based on exact match in name or notes"""
    pass


def pattern_search():
    """Searches for past entires based on an entered regex pattern"""
    pass
