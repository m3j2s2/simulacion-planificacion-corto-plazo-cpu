from Proceso import Proceso
from Strategy import Strategy
class Procesador:
    def __init__(self,TIP:int,TCP:int,TFP:int,strategy:Strategy )-> None:
        if not all(isinstance(valor, (int)) and valor >= 0 for valor in [TIP, TCP, TFP]):
            raise ValueError("TIP, TCP y TFP deben ser números no negativos.")
        if not isinstance(strategy, Strategy):
            raise TypeError("strategy debe ser una instancia de la clase Strategy.") 
        self.TIP = TIP  # Tiempo de Intercambio de Procesador
        self.TCP = TCP  # Tiempo de Cambio de Proceso   
        self.TFP = TFP  # Tiempo de Finalización de Proceso
        self.strategy = strategy
        self.Cola_de_Listos = []
        self.Cola_de_Espera = []
        self.Cola_de_Bloqueado = []
        self.Cola_de_Terminado = []
        self.ProcesoCargado : Proceso = None

    def Cargar_Procesos(self, procesos):
        if not isinstance(procesos, list):
            raise TypeError("La lista de procesos debe ser una lista.")
        if not all(isinstance(p, Proceso) for p in procesos):
            raise TypeError("Todos los elementos de la lista deben ser instancias de la clase Proceso.")
        self.Cola_de_Espera = procesos 

    def FinalizoSimulacion(self):
        if self.Cola_de_Listos == [] and self.Cola_de_Espera == [] and self.Cola_de_Bloqueado == []:
            return True
        return False

    def AceptarProcesos(self,tiempo):
        self.Cola_de_Espera.sort(key=lambda p: p.Proceso.tiempo_de_arribo)
        if self.Cola_de_Espera[0].Proceso.tiempo_de_arribo == tiempo:
            proceso = self.Cola_de_Espera.pop(0)
            self.Cola_de_Listos.append(proceso)
            tiempo+=self.TIP

    def EjecutarRafaga(self,tiempo):
        Strategy.ejecutar(self.TCP, self.TFP, self.tiempo, self.cola_de_terminados, self.cola_de_Bloqueados, self.cola_de_listos, self.proceso_cargado)    

    def simulacion(self):
        tiempo = 0
        while not self.FinalizoSimulacion():
            self.AceptarProcesos(tiempo)
            self.EjecutarRafaga(tiempo)
            tiempo += 1