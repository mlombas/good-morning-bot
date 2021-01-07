from time import sleep
from datetime import datetime, timedelta
from threading import Thread

class RepeatedTask(Thread):
    def __init__(self, task, time_of_repetition):
        self.task = task
        self.time_of_repetition = time_of_repetition

    def run(self):
        while True:
            now = datetime.now()
            next_timestamp = self.time_of_repetition.replace(day=now.day, month=now.month, year=now.year)
            if next_timestamp < now: next_timestamp += timedelta(days=1)

            sleep((next_timestamp - now).total_seconds())
            self.task()
