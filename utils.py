import datetime
import sys
import os
import pytz

import work_log
import add_task
import find_task


def clear_screen():
    """Clears the terminal screen to improve user experience"""
    os.system('cls' if os.name == 'nt' else 'clear')


def quit_program():
    """Funtion that quits the program at user's discretion"""
    clear_screen()
    print("Thanks for visiting the worklog!")
    sys.exit()


def footer_menu():
    """Displays the footer menu"""
    print("Choose An Option Below\n")
    while True:
        try:
            wrap_up = input("[M]ain Menu, [A]dd log, [S]earch logs, [Q]uit: ")
            if wrap_up.upper() == "M":
                work_log.main_menu()
            elif wrap_up.upper() == "A":
                add_task.Task()
            elif wrap_up.upper() == "S":
                find_task.search_options()
            elif wrap_up.upper() == "Q":
                clear_screen()
                quit_program()
            else:
                raise ValueError
        except ValueError:
            clear_screen()
            print("\n***PLEASE ENTER A VALID OPTION***\n")
        else:
            clear_screen()
            break


def utc_date(date):
    """Convert a date from user into UTC time"""
    date = datetime.datetime.strptime(date, "%m/%d/%Y")
    utc_date = date.astimezone(pytz.utc)
    return(utc_date)


