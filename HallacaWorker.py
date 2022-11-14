"""HallacaWorker is the base class for the people who are gonna
work for making the hallacas. This file also contains some
common variables the workers processes are gonna use."""


import sys
from shared_types import *
from working_table import get_working_table
from utils import ensure_locking, sleep, _sleep, normal
from settings import *


working_table = get_working_table((sys.argv[1], int(sys.argv[2])))

lock = working_table.lock()

leaf_stack = working_table.leaf_stack()
leaf_dough_stack = working_table.leaf_dough_stack()
to_tie_stack = working_table.to_tie_stack()

stop_order = working_table.stop_order()
dough_placing_stopped = working_table.dough_placing_stopped()
leaf_preparation_stopped = working_table.leaf_preparation_stopped()
stew_placing_stopped = working_table.stew_placing_stopped()


class HallacaWorker():
    def __init__(self, busy):
        self.busy = busy
        ready = working_table.ready()
        with lock:
            ready_value = ready.get()
            ready.set(ready_value + 1)
        # This ensures the other three processes are
        # also ready before start the simulation
        while True:
            with lock:
                if ready.get() == 4:
                    break
            _sleep(.1)

    @ensure_locking(lock)
    def work(self, **kwargs):
        """Sets the busy state of the worker to True"""
        self.busy.set(True)

    @ensure_locking(lock)
    def free(self, **kwargs):
        """Sets the busy state of the worker to False"""
        self.busy.set(False) 
