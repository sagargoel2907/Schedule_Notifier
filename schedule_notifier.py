import schedule
import random
from notifypy import Notify
import time
import threading
import sys
import json

def notify(task):
    tune_number=random.randint(1,17)
    notification=Notify()
    notification.title="Schedule Notifications"
    notification.message=task
    notification.audio=f"tune{tune_number}.wav"
    notification.icon="icon.png"
    notification.send(block=False)


def scheduler():
    while(True):
        n=schedule.idle_seconds()
        schedule.run_pending()


def load_saved_tasks():
    with open("tasks.json","r+") as fp:
        # tasks=json.dump([2,3],fp)
        try:
            tasks=json.loads(fp.read())
            return tasks
        except:return []

def schedule_saved_tasks(saved_tasks):
    for i in saved_tasks:
        task,time=i
        schedule.every().day.at(time).do(notify,task=task)

def main():
    print("-"*50)
    print("Welcome to Schedule Notifier program.\nIf you want to close the program then you can press Q or q any time.")
    print("-"*50)
    saved_tasks=load_saved_tasks()
    schedule_saved_tasks(saved_tasks)
    print("Saved tasks from your last session has been scheduled.")
    print("-"*50)
    print("If you want to add any task to the schedule then please enter the task and it's time separated by @")
    print("-"*50)
    notify_thread=threading.Thread(target=scheduler)
    notify_thread.daemon=True
    notify_thread.start()
    while(True):
        command=input()
        if command=="Q" or command=="q":
            #sys.exit()
            with open("tasks.json","w+") as fp:
                json.dump(saved_tasks,fp)
            break
        task,time=command.split("@")
        time=time.strip()
        schedule.every().day.at(time).do(notify,task=task)
        saved_tasks.append((task,time))
        print("Task Scheduled.")

if __name__=="__main__":
    main()