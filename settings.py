"""Settings for the simulation"""


# Constants config
M1, M2, M3, M4 = 10, 5, 6, 5
D1, D2, D3, D4 = 3, 1.5, 2, 2
X, Y = 5.23, 1000

# Simulation speed (simulation_time = real_time * speed)
speed = 10

# Importing the auth key for client-server authentication
try:
    from local_settings import AUTH_KEY
except ModuleNotFoundError as e:
    e.msg += "\n\nPlease create a local_settings.py file with the AUTH_KEY variable on it with a string literal as value\n"
    raise e
except ImportError as e:
    e.msg += "\n\nPlease configure the local_settings.py file with the AUTH_KEY variable on it with a string literal as value\n"
    raise e

AUTH_KEY = bytes(AUTH_KEY, 'utf-8')
