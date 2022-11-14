"""Process that gives a user interface to request the queries"""


import sys
from working_table import get_working_table
from utils import clear


working_table = get_working_table((sys.argv[1], int(sys.argv[2])))
query_tied = working_table.query_tied()
query_to_tie = working_table.query_to_tie()
query_stats = working_table.query_stats()
query_quit = working_table.query_quit()
lock = working_table.lock()

menu_message = """Seleccione una acción:
  (1) Imprimir cantidad de hallacas amarradas
  (2) Imprimir cantidad de hallacas por amarrar
  (3) Mostrar estadísticas
  (q) Salir

acción: """

while True:
    clear()
    action = input(menu_message)
    if len(action)!=1 or action.lower() not in '123q':
        continue
    with lock:
        if action == '1':
            query_tied.set(True)
        elif action == '2':
            query_to_tie.set(True)
        elif action == '3':
            query_stats.set(True)
        else:
            query_quit.set(True)
            print('\ncerrando...')
            break
