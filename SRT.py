from Procesador import Procesador
from Procesos import Proceso


class SRT(Procesador):
    def __init__(self, TIP: int, TCP: int, TFP: int, Quantum: int, Cola_de_Espera: list[Proceso]) -> None:
        super().__init__(TIP, TCP, TFP, Quantum, Cola_de_Espera)

    def OrdernarLaColadeListosPorRafaga(self):
        self.Cola_de_Listos.sort(key=lambda x: x.get_Tiempo_de_Rafaga_Restante())

    def simulacion(self):
        self.tiempo = 0     
        while not self.FinalizoSimulacion():
            self.AceptarProcesos()
            if self.Cola_de_Listos:                                ## si hay procesos en la cola de listos
                self.OrdernarLaColadeListosPorRafaga()             ## oredno la cola de listos por rafaga de cpu
                self.ProcesoCargado = self.Cola_de_Listos[0]       ## elijo el primer proceso de la cola de listos(el mas corto debido el ordenamiento)
                self.ProcesoCargado.registrar_evento(self.tiempo,self.TCP,'tcp')
                for _ in range(self.TCP): self.Decrementar_Tiempos_bloqueados() ## decremento los tiempos de los procesos bloqueados mientras espero el tcp
                self.OrdernarLaColadeListosPorRafaga()
                while self.ProcesoCargado == self.Cola_de_Listos[0] or self.ProcesoCargado.get_Tiempo_de_Rafaga_Restante()>0 :
                    self.ProcesoCargado.Consumir_Rafaga()
                    self.Decrementar_Tiempos_bloqueados()
                    self.tiempo+=1
                    self.AceptarProcesos()
                    self.OrdernarLaColadeListosPorRafaga
                if self.ProcesoCargado.get_Tiempo_de_Rafaga_Restante()==0 :
                    if  self.ProcesoCargado.get_Rafagas_restantes() > 0:     ## si quedan rafagas, lo bloqueo
                        self.Cola_de_Bloqueado.append(self.ProcesoCargado)  
                        self.ProcesoCargado.registrar_evento(self.tiempo,self.ProcesoCargado.get_Duracion_de_Entrada_Salida(),"Entrada/Salida") ##registo el e/s
                    else:
                        self.Cola_de_Terminado.append(self.ProcesoCargado) ## si no quedan rafagas, lo termino
                        self.ProcesoCargado.registrar_evento(self.tiempo,self.TFP,"Finalizacion")
                        self.tiempo += self.TFP
            else :
                self.tiempo += 1
                self.Decrementar_Tiempos_bloqueados()
        self.Cola_de_Terminado.sort(key=lambda x: x.get_Tiempo_de_Arribo())






























































