import threading
import queue

import Threading.threads as mythreads # Initializes global flags

#TODO: Implement pool for threads.

def launcher():
    myq = queue.Queue()
    ## Main run variables:
    mypop               = None
    application_runtime = None

    ## Defining threads:
    evol_     = threading.Thread(target = mythreads.evolver, name = 'evol_thread' ,args = (myq, mypop, application_runtime))
    control_  = threading.Thread(target = mythreads.get_input, name = 'control_thread')

    ## Launching threads:
    evol_.start()
    control_.start()

    ## Waiting for threads to terminate:
    evol_.join()
    control_.join()

    ## Getting queued output arguments from evol_:
    mypop, application_runtime = myq.get()

    return mypop, application_runtime
