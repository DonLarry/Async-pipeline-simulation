"""Code for the StewPlacer process"""


from HallacaWorker import *


class StewPlacer(HallacaWorker):
    stew = X * 1000

    def prepare(self):
        """Prepares the hallaca and returns it"""
        self.work()
        delay = normal(M3, D3)
        with lock:
            print('[3.a] colocando el guiso')
            hallaca = leaf_dough_stack.pop()
        sleep(delay)
        self.stew -= 80
        hallaca.stew = True
        self.free()
        return hallaca

    @ensure_locking(lock)
    def put(self, hallaca, **kwargs):
        """Puts the hallaca in the third stack"""
        print('[3.b] colocando hoja con guiso en -> pila de "por amarrar"')
        to_tie_stack.push(hallaca)

    @ensure_locking(lock)
    def order_stop(self, **kwargs):
        """Orders the leaf preparator to stop"""
        print('[3.c] ordenando al encargado de preparar las hojas que se detenga')
        stop_order.set(True)

    @ensure_locking(lock)
    def stop(self, **kwargs):
        self.order_stop(locked=True)
        print('[3.d] --- proceso de poner guiso detenido ---')
        stew_placing_stopped.set(True)

    def enough_stew(self):
        """Checks if there's enough stew for the hallacas or if there's less than Y grs of stew."""
        if self.stew <= Y:
            print(f"Menos de {Y}g de guiso! -> parando (regla de la simulación)")
            return False
        if self.stew < 80:
            print("Menos de 80g de guiso! -> parando (imposible seguir)")
            return False
        return True

    def start(self):
        """Colocación del guiso"""
        enough_stew = self.enough_stew()
        
        while enough_stew:
            with lock:
                empty = len(leaf_dough_stack) == 0
            #     if empty and dough_placing_stopped.get():
            #         self.stop(locked=True)
            #         break
            if empty:
                sleep(1)
                continue
            # with lock:
            #     if self.stew < 80:
            #         if not stop_order.get():
            #             print("Menos de 80g de guiso! -> parando (imposible seguir)")
            #             self.order_stop(locked=True)
            #         self.stop(locked=True)
            #         break
            hallaca = self.prepare()
            self.put(hallaca)
            enough_stew = self.enough_stew()
        self.stop()


StewPlacer(working_table.busy3()).start()
input('')
