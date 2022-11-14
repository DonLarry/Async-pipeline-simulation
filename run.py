"""Runs the simulation of the process of making hallacas"""


import sys
from time import sleep
from subprocess import (
    Popen,
    CalledProcessError,
    PIPE,
    CREATE_NEW_CONSOLE,
)
from working_table import get_working_table
from utils import clear, colored


workers_filenames = (
    'LeafPreparator.py',
    'DoughPlacer.py',
    'StewPlacer.py',
    'HallacaTier.py',
)


def is_debug_mode():
    """Returns true if debug flag is used as argument"""
    for arg in sys.argv:
        if arg == '-d' or arg == '--debug':
            return True
    return False


def run_server():
    """Runs the server and returns the server process"""
    cmd = [sys.executable, '-u', 'server.py']
    server_process = Popen(
        args=cmd,
        stdout=PIPE,
        universal_newlines=True,
    )

    def get_output():
        """Yields the output of the server process which must
        be its address on the network."""
        for stdout_line in iter(server_process.stdout.readline, ''):
            yield stdout_line
        server_process.stdout.close()
        return_code = server_process.wait()
        if return_code:
            raise CalledProcessError(return_code, cmd)

    # getting the only output line which comes trough the PIPE.
    for line in get_output():
        break
    return server_process, line.rstrip().split()


def start_processes(**workers_kw):
    """Runs the client processes for the simulation"""
    workers = [
        Popen(
            [sys.executable, filename, *address],
            creationflags=CREATE_NEW_CONSOLE,
            **workers_kw,
        ) for filename in workers_filenames
    ]
    interface = Popen(
        [sys.executable, 'query_client.py', *address],
        creationflags=CREATE_NEW_CONSOLE,
    )
    return interface, workers


def state_to_str(is_busy):
    """Returns the string representation of the state"""
    return 'ocupado' if is_busy else 'libre'


def get_states(lock, busy1, busy2, busy3, busy4):
    """Returns the values of the states"""
    with lock:
        return busy1.get(), busy2.get(), busy3.get(), busy4.get()


def print_states(*states):
    """Prints states of workers (libre / ocupado)"""
    workers_names = (
        '  Preparador de hojas:',
        '    Colocador de masa:',
        '   Colocador de guiso:',
        'Amarrador de hallacas:',
    )
    states_str = [state_to_str(states[i]) for i in range(4)]
    for to_print in zip(workers_names, states_str):
        print(*to_print)


def show_status(url, port):
    """Shows status of the workers until they stop"""

    working_table = get_working_table((url, int(port)))

    busy1 = working_table.busy1()
    busy2 = working_table.busy2()
    busy3 = working_table.busy3()
    busy4 = working_table.busy4()
    lock = working_table.lock()

    while not sum(get_states(lock, busy1, busy2, busy3, busy4)):
        sleep(.1)

    free_time = 0
    while free_time < 3:
        sleep(.2)
        clear()
        states = get_states(lock, busy1, busy2, busy3, busy4)
        if not sum(states):
            free_time += 1
        elif free_time:
            free_time = 0
        print_states(*states)
    clear()


server_process, address = run_server()

workers_kw = {}

# In debug mode, the outputs and errors of the workers are displayed
# in this process after finishing the simulation
DEBUG = is_debug_mode()

# We communicate with stdout and stderr of processes by using pipes
if DEBUG:
    workers_kw = {
        'universal_newlines': True,
        'stdout': PIPE,
        'stderr': PIPE,
    }

interface, workers = start_processes(**workers_kw)
show_status(*address)
print('Simulación terminada')
message = 'Presione Enter para terminar todos los procesos\n'
input(colored(0, 255, 0, message))
print('Terminando procesos...')

if DEBUG:
    for worker, filename in zip(workers, workers_filenames):
        worker.kill()
        outs, errs = worker.communicate()
        print('#'*10, filename, worker.pid, '#'*10)
        print(outs, errs, sep='\n\n')
else:
    for worker in workers:
        worker.kill()

interface.kill()
server_process.kill()
