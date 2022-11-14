"""Code for the LeafPreparatpr process"""


from HallacaWorker import *


class LeafPreparator(HallacaWorker):
    hallaca_id = 0

    def prepare(self):
        """Prepares the hallaca and returns it"""
        self.work()
        self.hallaca_id += 1
        hallaca = Hallaca(self.hallaca_id)
        delay = normal(M1, D1)
        sleep(delay)
        hallaca.leaf = True
        self.free()
        return hallaca

    @ensure_locking(lock)
    def put(self, hallaca, **kwargs):
        """Puts the hallaca in the first stack"""
        print('[1.b] colocando hoja en -> pila de hojas')
        leaf_stack.push(hallaca)

    @ensure_locking(lock)
    def stop(self, **kwargs):
        print('[1.c] --- proceso de preparación de hojas detenido ---')
        leaf_preparation_stopped.set(True)

    def start(self):
        """Starts the simulation of the leaf preparator"""
        while True:
            hallaca = self.prepare()
            with lock:
                if stop_order.get():
                    self.stop(locked=True)
                    break
            self.put(hallaca)

LeafPreparator(working_table.busy1()).start()
input('')
