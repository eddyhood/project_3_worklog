import csv
import logging
import datetime
import os

import utils


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
                utc_task_date = utils.utc_date(date)
            except ValueError:
                print("Pleae Enter a valid date in the format MM/DD/YYYY")
            else:
                logger.info("Valid date created as {}".format(utc_task_date))
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
        self.task_date_utc = utc_task_date
        self.task_time = task_time
        self.task_note = task_note
        self.task_timestamp = timestamp

        # Call functions to write task to file and show success
        self.write_task()
        self.success_add()

    def write_task(self):
        filename = "tasklogs.csv"
        temp_file = "task_temp.csv"
        with open(filename) as csvin, open(temp_file, "w") as csvout:
            reader = csv.DictReader(csvin)
            fieldnames = ["Task Name", "Task Date", "Task Date UTC",
                          "Task Time", "Task Note", "Task Timestamp"]
            writer = csv.DictWriter(csvout, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                writer.writerow(row)
            writer.writerow({
                "Task Name": self.task_name,
                "Task Date": self.task_date,
                "Task Date UTC": self.task_date_utc,
                "Task Time": self.task_time,
                "Task Note": self.task_note,
                "Task Timestamp": self.task_timestamp,
                })
            writer.writerows(reader)
        os.remove(filename)
        os.rename(temp_file, filename)
        utils.clear_screen()

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
        utils.footer_menu()
