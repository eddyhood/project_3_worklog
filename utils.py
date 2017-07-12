import sys
import os


def clear_screen():
    """Clears the terminal screen to improve user experience"""
    os.system('cls' if os.name == 'nt' else 'clear')


def quit_program():
    clear_screen()
    print("Thanks for visiting the worklog!")
    sys.exit()
