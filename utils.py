import os


def clear_screen():
    """Clears the terminal screen to improve user experience"""
    os.system('cls' if os.name == 'nt' else 'clear')
