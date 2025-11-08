from Procesador import Procesador
from Procesos import Proceso


class Prioridad(Procesador):
    def __init__(self, TIP: int, TCP: int, TFP: int, Quantum: int, Cola_de_Espera: list[Proceso]) -> None:
        super().__init__(TIP, TCP, TFP, Quantum, Cola_de_Espera)

    def OrdernarLaColadeListosPorPrioridad(self):
        self.Cola_de_Listos.sort(key=lambda x: x.get_Prioridad_Externa(), reverse=True)

    def simulacion(self):
        self.tiempo = 0     
        while not self.FinalizoSimulacion():
            self.AceptarProcesos()
            if self.Cola_de_Listos:                                ## si hay procesos en la cola de listos
                self.OrdernarLaColadeListosPorPrioridad()             ## oredno la cola de listos por prioridad
                ProcesoCargado = self.Cola_de_Listos[0]   ## elijo el primer proceso de la cola de listos(el mas corto debido el ordenamiento)
                ProcesoCargado.registrar_evento(self.tiempo,self.TCP,'tcp')
                self.registro_eventos.registrar_carga_proceso(self.tiempo, ProcesoCargado.nombre)
                for _ in range(self.TCP): 
                    self.tiempo += 1
                    self.Decrementar_Tiempos_bloqueados()          ## decremento los tiempos de los procesos bloqueados mientras espero el tcp
                self.registro_eventos.registrar_fin_carga_proceso(self.tiempo, ProcesoCargado.nombre)
                inicio_de_evento = self.tiempo
                duracion_de_evento = 0
                while ProcesoCargado == self.Cola_de_Listos[0] and ProcesoCargado.get_Tiempo_de_Rafaga_Restante() > 0: ## a la que no concuerde el de mayot prioridad con el que esta cargado se corta
                    ProcesoCargado.Consumir_Rafaga() 
                    duracion_de_evento+=1
                    self.tiempo += 1
                    self.Decrementar_Tiempos_bloqueados()
                    self.OrdernarLaColadeListosPorPrioridad() # vuelvo a ordenar por los procesos que se desbloqueen tienen mayor prioridad
                if duracion_de_evento>0: 
                    self.registro_eventos.registrar_inicio_rafaga(inicio_de_evento, ProcesoCargado.nombre)
                    ProcesoCargado.registrar_evento(inicio_de_evento,duracion_de_evento,"cpu")
                    if ProcesoCargado.get_Tiempo_de_Rafaga_Restante() == 0 :
                        self.Cola_de_Listos.remove(ProcesoCargado)
                        ProcesoCargado.Reducir_Rafagas_restantes()         ## reduzco la cantidad de rafagas restantes
                        if ProcesoCargado.get_Rafagas_restantes() > 0:      ## si quedan rafagas, lo bloqueo
                            self.registro_eventos.registrar_proceso_bloqueado(self.tiempo, ProcesoCargado.nombre)
                            self.Cola_de_Bloqueado.append(ProcesoCargado)  
                            ProcesoCargado.registrar_evento(self.tiempo,ProcesoCargado.get_Duracion_de_Entrada_Salida(),"Entrada/Salida") ##registo el e/s
                        else:
                            self.Cola_de_Terminado.append(ProcesoCargado) ## si no quedan rafagas, lo termino
                            ProcesoCargado.registrar_evento(self.tiempo,self.TFP,"Finalizacion")
                            self.registro_eventos.registrar_proceso_empiza_TFP(self.tiempo, ProcesoCargado.nombre)
                            for _ in range(self.TFP):
                                self.tiempo += 1
                                self.Decrementar_Tiempos_bloqueados()
                            self.registro_eventos.registrar_proceso_terminado(self.tiempo, ProcesoCargado.nombre)
                    else: 
                        self.registro_eventos.registrar_corte_rafaga_prioridad(self.tiempo, ProcesoCargado.nombre,self.Cola_de_Listos[0].get_Nombre())
            else :
                self.tiempo += 1
                self.tiempo_Ocioso +=1
                self.Decrementar_Tiempos_bloqueados()
        self.Cola_de_Terminado.sort(key=lambda x: x.get_Tiempo_de_Arribo())