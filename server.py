"""This process will host and serve the data that is gonna be shared between the processes"""


import multiprocessing
import threading
from shared_types import *
from settings import AUTH_KEY


# Creates the memory manager (the port is assigned by the OS)
working_table = WorkingTable(address=('localhost', 0), authkey=AUTH_KEY)


def register_variable(typeid, value=None):
    """Registers an instance of the class Var in the memory manager"""
    var = Var(value)
    working_table.register(typeid, callable=lambda:var, exposed=('get', 'set'))
    return var


def register_stack(typeid):
    """Registers a stack in the memory manager"""
    var = Stack()
    working_table.register(typeid, callable=lambda:var, exposed=('__len__', 'push', 'pop'))
    return var


lock = multiprocessing.Lock()

# Registering all the shared variables
working_table.register('lock', lambda:lock, exposed=('__enter__', '__exit__', 'acquire', 'release'))
leaf_stack = register_stack('leaf_stack')
leaf_dough_stack = register_stack('leaf_dough_stack')
to_tie_stack = register_stack('to_tie_stack')
stop_order = register_variable('stop_order', False)
leaf_preparation_stopped = register_variable('leaf_preparation_stopped', False)
dough_placing_stopped = register_variable('dough_placing_stopped', False)
stew_placing_stopped = register_variable('stew_placing_stopped', False)
to_rie_query = register_variable('to_rie_query', False)
already_tied_query = register_variable('already_tied_query', False)
busy1 = register_variable('busy1', False)
busy2 = register_variable('busy2', False)
busy3 = register_variable('busy3', False)
busy4 = register_variable('busy4', False)
ready = register_variable('ready', 0)
query_tied = register_variable('query_tied', False)
query_to_tie = register_variable('query_to_tie', False)
query_stats = register_variable('query_stats', False)
query_quit = register_variable('query_quit', False)


server = working_table.get_server()
thread = threading.Thread(target=server.serve_forever)
# The run.py process will get the address trough a PIPE
# (this is necessary because the port is not static, but assigned by the OS)
print(*server.address)
thread.start()
