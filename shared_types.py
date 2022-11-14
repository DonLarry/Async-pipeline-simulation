"""This file defines the WorkingTable class and the types that are
gonna be shared between the processes by using the working table"""


from time import time
from multiprocessing.managers import BaseManager


class WorkingTable(BaseManager):
    """WorkingTable is a BaseManager (memory manager) as the memory manager could be seen as the memory itself"""
    pass


class Var:
    """Simple variable class with get and set methods"""
    def __init__(self, value=None):
        self._value = value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

    value = property(get, set)


class Hallaca():
    """An hallaca either finished or in process its creation"""
    id = None
    started_at = None
    finished_at = None
    leaf = False
    dough = False
    stew = False
    tied = False

    def __init__(self, id):
        self.id = id
        self.started_at = time()

    def __str__(self):
        return f'<Hallaca #{self.id}>'


class Stack():
    """A simple stack class"""
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def push(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop()
