"""Code for the DoughPlacer process"""


from HallacaWorker import *


class DoughPlacer(HallacaWorker):
    def prepare(self):
        """Prepares the hallaca and returns it"""
        self.work()
        delay = normal(M2, D2)
        with lock:
            print('[2.a] colocando masa')
            hallaca = leaf_stack.pop()
        sleep(delay)
        hallaca.dough = True
        self.free()
        return hallaca

    @ensure_locking(lock)
    def put(self, hallaca, **kwargs):
        """Puts the hallaca in the second stack"""
        print('[2.b] colocando hoja con masa en -> pila de hojas con masa')
        leaf_dough_stack.push(hallaca)

    @ensure_locking(lock)
    def stop(self, **kwargs):
        print('[2.c] --- proceso de poner masa detenido ---')
        dough_placing_stopped.set(True)

    def start(self):
        """Starts the simulation of the dough placer"""
        while True:
            with lock:
                empty = len(leaf_stack) == 0
                if empty and leaf_preparation_stopped.get():
                    self.stop(locked=True)
                    break
            if empty:
                sleep(1)
                continue
            hallaca = self.prepare()
            self.put(hallaca)

DoughPlacer(working_table.busy2()).start()
input('')
