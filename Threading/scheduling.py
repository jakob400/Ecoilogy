def scheduler(*args):
    trials          = args[0]
    radius          = args[1]
    mutation_method = [2]
    concurrent_max  = [3]

class Scheduler:
    ID_list = []
    def __init__(self):
    def launch_trial(self, trial_ID):
    def exit_trial(self, trial_ID):


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
