from time import sleep
from datetime import datetime, timedelta
from threading import Thread

class RepeatedTask():
    def __init__(self, task=None, time_of_repetition=None):
        self.task = task
        self.time_of_repetition = time_of_repetition
        self.thread = None
    
    def restart(self):
        if self.thread: self.thread.stop()
        self.thread = StoppableThread(self.task, self.time_of_repetition) 
        print(self.time_of_repetition)
        self.thread.start()

    def is_alive(self):
        return self.thread and self.thread.is_alive()

class StoppableThread(Thread):
    def __init__(self, task=None, time_of_repetition=None):
        super().__init__()
        self.task = task
        self.time_of_repetition = time_of_repetition
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running and self.task and self.time_of_repetition:
            now = datetime.now()
            next_timestamp = self.time_of_repetition.replace(day=now.day, month=now.month, year=now.year)
            if next_timestamp < now: next_timestamp += timedelta(days=1)

            sleep((next_timestamp - now).total_seconds())
            if self.running:
                self.task()
