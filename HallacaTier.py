"""Code for the HallacaTier process"""


from HallacaWorker import *
from matplotlib import pyplot as plt
from time import sleep as _sleep
import threading
from utils import colored, yellow, blue, red
from bisect import insort


query_tied = working_table.query_tied()
query_to_tie = working_table.query_to_tie()
query_stats = working_table.query_stats()
query_quit = working_table.query_quit()


class HallacaTier(HallacaWorker):
    hallacas = []
    starting_time = None

    def __init__(self, busy, thread_lock):
        super().__init__(busy)
        self.thread_lock = thread_lock
        self.stopped = False
        self.queries = query_tied, query_to_tie, query_stats
        self.actions = self.action_query_tied, self.action_query_to_tie, self.action_query_stats

    def prepare(self):
        """Prepares the hallaca and returns it"""
        self.work()
        delay = normal(M4, D4)
        with lock:
            self.print('[4.a] amarrando hallaca')
            hallaca = to_tie_stack.pop()
        sleep(delay)
        hallaca.tied = True
        starting_time = self.starting_time
        if starting_time is None:
            starting_time = self.starting_time = hallaca.started_at
        hallaca.started_at = (hallaca.started_at - starting_time) * speed
        hallaca.finished_at = (time() - starting_time) * speed
        self.free()
        return hallaca

    def put(self, hallaca):
        """Saves the hallaca into an array in sorted order"""
        with lock:
            insort(self.hallacas, hallaca, key=lambda x: x.id)
        self.print(f'[4.b] hallaca "{hallaca}" amarrada')

    def stop(self):
        with self.thread_lock:
            self.stopped = True
            print('[4.c] --- proceso de amarrar hallacas detenido ---')

    def print(self, *args, **kwargs):
        """Thread safe print function"""
        with self.thread_lock:
            print(*args, **kwargs)

    def len(self, obj):
        """Thread safe len function"""
        with self.thread_lock:
            return len(obj)

    def action_query_tied(self):
        """Performs the action related to the query_tied query"""
        m1 = colored(*yellow, "Respuesta de query:")
        m2 = str(self.len(self.hallacas))
        m3 = colored(*yellow, "hallacas hechas.")
        messages = m1, m2, m3
        self.print(*messages)

    def action_query_to_tie(self):
        """Performs the action related to the query_to_tie query"""
        m1 = colored(*yellow, "Respuesta de query:")
        m2 = str(self.len(to_tie_stack))
        m3 = colored(*yellow, "hallacas por amarrar.")
        messages = m1, m2, m3
        self.print(*messages)

    def action_query_stats(self):
        """Performs the action related to the query_stats query"""
        if self.len(self.hallacas):
            self.statistics()
        else:
            self.print(colored(*yellow, "Respuesta de query: No hay hallacas para mostrar estadísticas."))

    def check_queries(self):
        """Respond to requested queries"""
        for i in range(3):
            with lock:
                perform = self.queries[i].get()
            if not perform:
                continue
            self.actions[i]()
            with lock:
                self.queries[i].set(False)

    def stat_1(self):
        """Plot with hallaca's starting (blue) and fihishing (red) time"""
        hallacas = self.hallacas
        m1 = colored(*blue, 'Azul:')
        m2 = colored(*yellow, 'momento en el que se empieza a hacer la hallaca')
        self.print(m1, m2)
        m1 = colored(*red, 'Rojo:')
        m2 = colored(*yellow, 'momento en el que la hallaca es finalmente amarrada')
        self.print(m1, m2)
        plt.plot([hallaca.started_at for hallaca in hallacas], 'o')
        plt.plot([hallaca.finished_at for hallaca in hallacas], 'o', color='r')
        plt.xlabel('Hallaca creada (ordenadas por orden de creación)')
        plt.ylabel('Tiempo (segundos)')
        plt.show()

    def stat_2(self):
        """Histogram of the time it takes to create each hallaca"""
        hallacas = self.hallacas
        plt.hist(
            [hallaca.finished_at - hallaca.started_at for hallaca in hallacas],
            color='#8F3C5A',
        )
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Hallacas')
        plt.show()

    def statistics(self):
        """Shows statistics"""
        self.stat_1()
        self.stat_2()
        total_time = self.hallacas[-1].finished_at
        m1 = "Tiempo total haciendo hallacas:"
        m2 = f"{total_time:.2f} s"
        messages = colored(*yellow, m1), m2
        self.print(*messages)

    def listen_queries(self):
        """Keeps listening for queries"""
        quit = False
        while not quit:
            self.check_queries()
            _sleep(.2)
            with lock:
                quit = query_quit.get()

    def start(self):
        """Starts the simulation of the hallaca tier"""
        while True:
            with lock:
                empty = len(to_tie_stack) == 0
                flag = empty and stew_placing_stopped.get()
            if flag:
                self.stop()
                break
            if empty:
                sleep(1)
                continue
            hallaca = self.prepare()
            self.put(hallaca)

hallaca_tier = HallacaTier(working_table.busy4(), threading.Lock())
t1 = threading.Thread(target=hallaca_tier.start)
t1.start()
hallaca_tier.listen_queries()
t1.join()
input('')
