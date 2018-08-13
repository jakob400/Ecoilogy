from concurrent.futures import ThreadPoolExecutor
import threading

def scheduler(*args):
    trials          = args[0]
    radius          = args[1]
    mutation_method = [2]
    concurrent_max  = [3]

    executor = ThreadPoolExecutor(max_workers = concurrent_max)


class Scheduler:
    ID_list = []
    def __init__(self, trials):
    def launch_trial(self):
    def exit_trial(self):


class Trial:
    ID                  = None
    myqueue             = None
    mypop               = None
    application_runtime = None

    def __init__(self, trial_ID, queueop):
        self.ID = trial_ID
        self.myqueue = queueop

        evol_     = threading.Thread(target = mythreads.evolver, name = self.ID ,args = (queueop, mypop, application_runtime))
    def launch():

Master = Scheduler():
Master.launch_trial
