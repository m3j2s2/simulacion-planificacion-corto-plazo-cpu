from Procesador import Procesador
from Procesos import Proceso


class FCFS(Procesador):
    def __init__(self, TIP: int, TCP: int, TFP: int, Quantum: int, Cola_de_Espera: list[Proceso]) -> None:
        super().__init__(TIP, TCP, TFP, Quantum, Cola_de_Espera)

    def simulacion(self):
        tiempo = 0
        while not self.FinalizoSimulacion():
            self.AceptarProcesos(tiempo)
            if self.Cola_de_Listos: ## si hay procesos en la cola de listos
                self.ProcesoCargado = self.Cola_de_Listos.pop(0) ## elijo el primer proceso de la cola de listos
                for _ in range(self.TCP):  ## cargo el proceso y por lo tanto cuento el tiempo de cambio de proceso (tcp)
                    tiempo += 1 
                    self.Decrementar_Tiempos_bloqueados() ### decremento los tiempos de los procesos bloqueados mientras espero el tcp
                for _ in range(int(self.ProcesoCargado.get_Duracion_de_Rafaga())): ## ejecuto toda la rafaga
                    self.ProcesoCargado.Consumir_Rafaga() 
                    tiempo += 1
                self.ProcesoCargado.Reducir_Rafagas_restantes() ## reduzco la cantidad de rafagas restantes
                if self.ProcesoCargado.get_Rafagas_restantes() > 0: ## si quedan rafagas, lo bloqueo
                    self.Cola_de_Bloqueado.append(self.ProcesoCargado)
                else:
                    self.Cola_de_Terminado.append(self.ProcesoCargado) ## si no quedan rafagas, lo termino
                self.ProcesoCargado = None
            tiempo += 1


            