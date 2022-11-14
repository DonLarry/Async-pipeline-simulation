"""Comfortable way of getting the working table"""


from shared_types import WorkingTable
from settings import AUTH_KEY


to_register = (
    'lock',
    'leaf_stack',
    'leaf_dough_stack',
    'to_tie_stack',
    'stop_order',
    'dough_placing_stopped',
    'leaf_preparation_stopped',
    'stew_placing_stopped',
    'busy1',
    'busy2',
    'busy3',
    'busy4',
    'query_tied',
    'query_to_tie',
    'query_stats',
    'query_quit',
    'ready',
    'starting_time',
)


def get_working_table(address, authkey=AUTH_KEY):
    """Returns an instance of the working table"""
    working_table = WorkingTable(address=address, authkey=authkey)
    for typeid in to_register:
        working_table.register(typeid)
    working_table.connect()
    return working_table
