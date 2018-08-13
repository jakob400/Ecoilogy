from concurrent.futures import ThreadPoolExecutor
import threading
import random
import time

def task():
    print("Task Launched {}".format(threading.current_thread()))
    time.sleep(5)
    print("Task Executed {}".format(threading.current_thread()))

def main():
    tasklist = []
    executor = ThreadPoolExecutor(max_workers=3)
    for i in range(10):
        tasklist.append(executor.submit(task))

main()
