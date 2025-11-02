from abc import abstractmethod
from Procesos import Proceso
class Procesador:
    def __init__(self,TIP:int,TCP:int,TFP:int,Quantum:int,Cola_de_Espera : list[Proceso])-> None:
        if not all(isinstance(valor, (int)) and valor >= 0 for valor in [TIP, TCP, TFP, Quantum]):
            raise ValueError("TIP, TCP, TFP y Quantum deben ser números enteros no negativos.")
        if not isinstance(Cola_de_Espera, list):
            raise TypeError("Cola_de_Espera debe ser una lista de procesos.")
            if not all(isinstance(p, Proceso) for p in Cola_de_Espera):
                raise TypeError("Todos los elementos de Cola_de_Espera deben ser instancias de la clase Proceso.")
        self.TIP = TIP  # Tiempo de Intercambio de Procesador
        self.TCP = TCP  # Tiempo de Cambio de Proceso   
        self.TFP = TFP  # Tiempo de Finalización de Proceso
        self.Quantum = Quantum  # Tiempo de Quantum
        self.Cola_de_Listos : list[Proceso] = []
        self.Cola_de_Espera : list[Proceso] = Cola_de_Espera
        self.Cola_de_Bloqueado  : list[Proceso] = []
        self.Cola_de_Terminado : list[Proceso]= []
        self.ProcesoCargado : Proceso
        self.tiempo = 0

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

    def Decrementar_Tiempos_bloqueados(self):
        for proceso in self.Cola_de_Bloqueado:
            proceso.reducir_Tiempo_de_Entrada_Salida_Restante()
            if proceso.get_Duracion_de_Entrada_Salida_Restante() == 0:
                proceso.reset_Tiempo_de_Entrada_Salida_Restante()
                self.Cola_de_Bloqueado.remove(proceso)
                self.Cola_de_Listos.append(proceso)


    def AceptarProcesos(self):
        self.Cola_de_Espera.sort(key=lambda p: p.tiempo_de_arribo)
        if self.Cola_de_Espera and self.Cola_de_Espera[0].tiempo_de_arribo <= self.tiempo:
            proceso = self.Cola_de_Espera.pop(0)
            inicio_de_evento=self.tiempo
            duracion_de_evento=0
            self.Cola_de_Listos.append(proceso)
            for _ in range(self.TIP):  ##una vez se acepta un proceso, se cuenta el tiempo de inicio de proceso (tip)
                duracion_de_evento+=1
                self.tiempo += 1
                self.Decrementar_Tiempos_bloqueados() ### decremento los tiempos de los procesos bloqueados mientras espero el tip
            proceso.registrar_evento(inicio_de_evento,duracion_de_evento,'tip')
            self.AceptarProcesos()  ##verifico si hay mas procesos para aceptar en el mismo tiempo

    @abstractmethod
    def simulacion(self):
        pass