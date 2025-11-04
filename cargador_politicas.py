from FCFS import FCFS
from SJF import SJF
from SRT import SRT
from RoundRobin import RoundRobin
from PrioridadPreemtiva import Prioridad

class CargarPoliticas:

    @staticmethod
    def crear_procesador(politica, tip, tcp, tfp, quantum, cola_espera):
        politica = politica.lower()

        if politica == "fcfs":
            return FCFS(tip, tcp, tfp, quantum, cola_espera)
        elif politica == "sjf":
            return SJF(tip, tcp, tfp, quantum, cola_espera)
        elif politica == "srt":
            return SRT(tip, tcp, tfp, quantum, cola_espera)
        elif politica == "prioridad preemtiva":
            return Prioridad(tip, tcp, tfp, quantum, cola_espera)
        elif politica == "round robin":
            return RoundRobin(tip, tcp, tfp, quantum, cola_espera)
        else:
            raise ValueError(f"Política desconocida: {politica}")
