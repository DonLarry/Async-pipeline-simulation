"""Utilities"""


import os
from functools import wraps
from time import sleep as _sleep, time as _time
from numpy.random import normal as _normal
from settings import speed


def ensure_locking(lock, locked=False):
    """Decorator that protects functions from race conditions"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _locked = locked
            if 'locked' in kwargs:
                _locked = kwargs['locked']
            if not _locked:
             lock.acquire()
             return_value = f(*args, **kwargs)
             lock.release()
             return return_value
            return f(*args, **kwargs)
        return wrapper
    return decorator


def sleep(time):
    """Sleep function for the simulation (the simulation time should not
    be necessarily the same as real time but could be accelerated)"""
    _sleep(time/speed)


def normal(loc=0, scale=1, size=None) -> float:
    """Draw random non-negative or null samples from a normal (Gaussian) distribution."""
    while True:
        value = _normal(loc, scale, size)
        if value > 0:
            return value


# Defining a function to clear the console depending on the OS
if os.name == "nt":
    # Windows
    def clear():
        """Clears the console"""
        os.system("cls")
    # If windows, also we should prepare to use colors
    os.system("color")
    clear()
else:
    # Linux or MacOS 
    def clear():
        """Clears the console"""
        os.system("clear")


# Defining some colors
yellow = 255, 255, 0
blue = 31, 119, 180
red = 255, 0, 0
white = 255, 255, 255
default = white


def colored(r, g, b, text):
    """Returns a colored string and resets the color to the default color"""
    return "\033[38;2;{};{};{}m{}\033[38;2;{};{};{}m".format(r, g, b, text, *default)


# Using the default color
print("\033[38;2;{};{};{}m".format(*default), end='')
