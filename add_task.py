import sys
import csv
import logging

import work_log
import find_task
import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logging_files/add_task.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


class Task:
    """Creates a class object for each task"""
    def __init__(self, *args, **kwagrs):
        utils.clear_screen()
        task_name = (input("Enter a task name: "))
        utils.clear_screen()
        task_date = (input("Enter the task date (Use MM/DD/YYYY): "))
        utils.clear_screen()
        task_time = (input("Enter the task duration in minutes: "))
        utils.clear_screen()
        task_note = (input("Enter a optional notes: "))

        self.task_name = task_name
        self.task_date = task_date
        self.task_time = task_time
        self.task_note = task_note
        logger.info("""User created a complete task with the following info:
                    Task Name: {}, Task Date: {}, Task Time: {},
                    Task Note: {}""".format(self.task_name, self.task_date,
                                            self.task_time, self.task_note))
        self.write_task()
        self.success_message()

    def write_task(self):
        """Writes the task to the log file"""
        with open("tasklogs.csv", "a") as csvfile:
            fieldnames = ["Task Name", "Task Date",
                          "Task Time", "Task Note"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                        "Task Name": self.task_name,
                        "Task Date": self.task_date,
                        "Task Time": self.task_time,
                        "Task Note": self.task_note
                        })
            csvfile.close()
            logger.info("Task {} was recorded in the log.".format
                        (self.task_name))

    def success_message(self):
        print("""You have successfully entered the following task:\n
              Task name: {}
              Task date: {}
              Task time: {}
              Task note: {}
              """.format(self.task_name, self.task_date, self.task_time,
                         self.task_note))
        try:
            wrap_up = input("[M]ain Menu, [A]dd task, [E]dit task, [Q]uit: ")
            if wrap_up.upper() == "M":
                work_log.main_menu()
            elif wrap_up.upper() == "A":
                Task()
            elif wrap_up.upper() == "E":
                find_task.search_options()
            elif wrap_up.upper() == "Q":
                utils.clear_screen()
                utils.quit_program()
        except ValueError:
            print("Please enter a valid option")

