import json
from Procesos import Proceso  # tu clase
from FCFS import FCFS

def cargar_procesos_desde_json(ruta_json: str) -> list[Proceso]:
    procesos = []
    
    with open(ruta_json, "r") as archivo:
        data = json.load(archivo)

    for p in data:
        duracion_es = p["duracion_rafaga_es"]
        
        # Evitar error por valores de E/S iguales a 0 en tu validador
        if duracion_es <= 0:
            duracion_es = 0.0001  

        proceso = Proceso(
            nombre=p["nombre"],
            tiempo_de_arribo=p["tiempo_arribo"],
            cantidad_de_rafagas=p["cantidad_rafagas_cpu"],
            duracion_de_rafaga=p["duracion_rafaga_cpu"],
            duracion_de_entrada_salida=duracion_es,
            prioridad_externa=p["prioridad_externa"]
        )
        procesos.append(proceso)

    simulador = FCFS(TIP=2, TCP=1, TFP=1, Quantum=4, Cola_de_Espera=procesos)
    simulador.simulacion()
    cola_terminados = simulador.Cola_de_Terminado

