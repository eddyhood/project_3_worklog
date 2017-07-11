import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler("logging_files/add_task.log")
file_handler.setFormatter(fmt)
logger.addHandler(file_handler)


def add_new():
    """Adds a new task into the worklog"""
    logger.info("User added a new task")
    print("This is where you add tasks")
