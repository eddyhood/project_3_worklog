import utils


def main_menu():
    """Displays the beginning main menu for the application"""
    utils.clear_screen()
    print("=============  Welcome to the Company Worklog!  =============\n")
    print("This program tracks events by name, date, time, and notes.\n" +
          "As an employee of Dunder Mifflin, please enjoy tracking every\n" +
          "aspect of your life.\n")
    utils.footer_menu()


if __name__ == "__main__":
    main_menu()
