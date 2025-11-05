from Procesador import Procesador
from Procesos import Proceso


class RoundRobin(Procesador):
    def __init__(self, TIP: int, TCP: int, TFP: int, Quantum: int, Cola_de_Espera: list[Proceso]) -> None:
        super().__init__(TIP, TCP, TFP, Quantum, Cola_de_Espera)
        
    def simulacion(self):
        self.tiempo = 0     
        while not self.FinalizoSimulacion():
            self.AceptarProcesos()
            if self.Cola_de_Listos:                                ## si hay procesos en la cola de listos
                ProcesoCargado = self.Cola_de_Listos[0]   ## elijo el primer proceso de la cola de listos(el mas corto debido el ordenamiento)
                inicio_de_evento=self.tiempo
                duracion_de_evento=0
                for _ in range(self.TCP):                          ## cargo el proceso y por lo tanto cuento el tiempo de cambio de proceso (tcp)
                    self.tiempo += 1
                    duracion_de_evento+=1                                                    
                    self.Decrementar_Tiempos_bloqueados()          ## decremento los tiempos de los procesos bloqueados mientras espero el tcp
                ProcesoCargado.registrar_evento(inicio_de_evento,duracion_de_evento,'tcp')
                inicio_de_evento = self.tiempo
                duracion_de_evento = 0
                quantum = self.Quantum
                while quantum > 0 and ProcesoCargado.get_Tiempo_de_Rafaga_Restante() > 0 : ## ejecuto toda la rafaga
                    ProcesoCargado.Consumir_Rafaga()
                    quantum-=1 
                    duracion_de_evento+=1
                    self.tiempo += 1
                ProcesoCargado.registrar_evento(inicio_de_evento,duracion_de_evento,"cpu")
                if ProcesoCargado.get_Tiempo_de_Rafaga_Restante() == 0:
                    self.Cola_de_Listos.remove(ProcesoCargado) 
                    ProcesoCargado.Reducir_Rafagas_restantes()         ## reduzco la cantidad de rafagas restantes
                    if ProcesoCargado.get_Rafagas_restantes() > 0:     ## si quedan rafagas, lo bloqueo
                        self.Cola_de_Bloqueado.append(ProcesoCargado)  
                        ProcesoCargado.registrar_evento(self.tiempo,ProcesoCargado.get_Duracion_de_Entrada_Salida(),"Entrada/Salida") ##registo el e/s
                    else:
                        self.Cola_de_Terminado.append(ProcesoCargado) ## si no quedan rafagas, lo termino
                        ProcesoCargado.registrar_evento(self.tiempo,self.TFP,"Finalizacion")
                        self.tiempo += self.TFP
            else :
                self.tiempo += 1
                self.Decrementar_Tiempos_bloqueados()
        self.Cola_de_Terminado.sort(key=lambda x: x.get_Tiempo_de_Arribo())