from Procesador import Procesador
from Procesos import Proceso


class FCFS(Procesador):
    def __init__(self, TIP: int, TCP: int, TFP: int, Quantum: int, Cola_de_Espera: list[Proceso]) -> None:
        super().__init__(TIP, TCP, TFP, Quantum, Cola_de_Espera)

    def simulacion(self):
        self.tiempo = 0     
        while not self.FinalizoSimulacion():
            self.AceptarProcesos()
            if self.Cola_de_Listos:                                ## si hay procesos en la cola de listos
                ProcesoCargado = self.Cola_de_Listos.pop(0)   ## elijo el primer proceso de la cola de listos
                inicio_de_evento=self.tiempo
                duracion_de_evento=0
                for _ in range(self.TCP):                          ## cargo el proceso y por lo tanto cuento el tiempo de cambio de proceso (tcp)
                    self.tiempo += 1
                    duracion_de_evento+=1                                                    
                    self.Decrementar_Tiempos_bloqueados()          ## decremento los tiempos de los procesos bloqueados mientras espero el tcp
                ProcesoCargado.registrar_evento(inicio_de_evento,duracion_de_evento,'tcp')
                inicio_de_evento = self.tiempo
                duracion_de_evento = 0
                for _ in range(int(ProcesoCargado.get_Duracion_de_Rafaga())): ## ejecuto toda la rafaga
                    ProcesoCargado.Consumir_Rafaga()
                    self.Decrementar_Tiempos_bloqueados()  
                    duracion_de_evento+=1
                    self.tiempo += 1
                ProcesoCargado.registrar_evento(inicio_de_evento,duracion_de_evento,"cpu")
                ProcesoCargado.Reducir_Rafagas_restantes()         ## reduzco la cantidad de rafagas restantes
                if ProcesoCargado.get_Rafagas_restantes() > 0:     ## si quedan rafagas, lo bloqueo
                    self.Cola_de_Bloqueado.append(ProcesoCargado)  
                    ProcesoCargado.registrar_evento(self.tiempo,ProcesoCargado.get_Duracion_de_Entrada_Salida(),"Entrada/Salida") ##registo el e/s
                else:
                    self.Cola_de_Terminado.append(ProcesoCargado) ## si no quedan rafagas, lo termino
                    ProcesoCargado.registrar_evento(self.tiempo,self.TFP,"Finalizacion")
                    self.tiempo += self.TFP
                    for _ in range(self.TFP): self.Decrementar_Tiempos_bloqueados()
                    ProcesoCargado.set_Tiempo_de_Retorno(self.tiempo) 
            else :
                self.tiempo += 1
                self.Decrementar_Tiempos_bloqueados()
        self.Cola_de_Terminado.sort(key=lambda x: x.get_Tiempo_de_Arribo())