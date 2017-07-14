import csv
import logging
import datetime

import find_task
import utils
import work_log

# Custom logger built to track task creation.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logs/add_task.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


class Task:
    """Creates a class object for each task"""
    def __init__(self, *args, **kwagrs):

        # Creates a name for the task as a string
        utils.clear_screen()
        print("==============  Add a New Work Log Here  ==============")
        task_name = (input("Enter a task name: "))
        logger.info("Task name created successfully as {}".format(task_name))

        # Gets date of task and converts it from string to datetime object
        while True:
            try:
                date = (input("Enter the task date (Use MM/DD/YYYY): "))
                task_date = datetime.datetime.strptime(str(date), "%m/%d/%Y")
            except ValueError:
                print("Pleae Enter a valid date in the format MM/DD/YYYY")
            else:
                logger.info("Valid date created as {}".format(task_date))
                break

        # Gets number of minutes task took and stores it as an int
        while True:
            try:
                task_time = (int(input("Enter the task time in minutes: ")))
            except ValueError:
                print("""Hmmm, that didn't work.  Enter a number only.""")
            else:
                logger.info("Valid time created as {}".format(task_time))
                break

        # Gets optional notes for task as a string
        task_note = (input("Enter a optional notes: "))
        logger.info("Valid note created as {}".format(task_note))

        # create a unique timestamp for when the task is created
        timestamp = datetime.datetime.now()

        # Assign attributes to the task instance & log creation
        self.task_name = task_name
        self.task_date = date
        self.task_date_dt = task_date
        self.task_time = task_time
        self.task_note = task_note
        self.task_timestamp = timestamp
        logger.info("""User created a complete task with the following info:
                    Task Name: {}, Task Date: {}, Task Time: {},
                    Task Note: {}""".format(self.task_name, self.task_date,
                                            self.task_time, self.task_note))
        # Call functions to write task to file and show success
        self.write_task()
        self.success_add()

    def write_task(self):
        """Writes the task to the log file"""
        with open("tasklogs.csv", "a", newline="") as csvfile:
            fieldnames = ["Task Name", "Task Date", "Task Date DT",
                          "Task Time", "Task Note", "Task Timestamp"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                        "Task Name": self.task_name,
                        "Task Date": self.task_date,
                        "Task Date DT": self.task_date_dt,
                        "Task Time": self.task_time,
                        "Task Note": self.task_note,
                        "Task Timestamp": self.task_timestamp,
                        })
            csvfile.close()
            logger.info("Task {} was recorded in the log.".format
                        (self.task_name))

    def success_add(self):
        """Prints a success message for when a task is added"""
        utils.clear_screen()
        print("""You have successfully entered the following task:\n
              Task name: {}
              Task date: {}
              Task time: {} minutes
              Task note: {}
              """.format(self.task_name, self.task_date, self.task_time,
                         self.task_note))
        try:
            print("What would you like to do next?")
            wrap_up = input("[M]ain Menu, [A]dd task, [S]earch task, [Q]uit: ")
            if wrap_up.upper() == "M":
                work_log.main_menu()
            elif wrap_up.upper() == "A":
                Task()
            elif wrap_up.upper() == "S":
                find_task.search_options()
            elif wrap_up.upper() == "Q":
                utils.clear_screen()
                utils.quit_program()
            else:
                raise ValueError
        except ValueError:
            utils.clear_screen()
            print("\n***PLEASE ENTER A VALID OPTION***\n")
            self.success_add()
