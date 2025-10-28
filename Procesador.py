
Cola_de_Listos = []
Cola_de_Espera = []
Cola_de_Bloqueado = []
Cola_de_Terminado = []
ProcesoCargado = None
tiempo = 0

def FinalizoSimulacion():
    if Cola_de_Listos == [] and Cola_de_Espera == [] and Cola_de_Bloqueado == []:
        return True
    return False

def AceptarProcesos(tiempo):
    global ProcesoCargado
    if Cola_de_Listos[0].Proceso.tiempo_de_arribo == tiempo:
        proceso = Cola_de_Listos.pop(0)
        Cola_de_Listos.append(proceso)
        ProcesoCargado = proceso

def EjecutarRafaga():
    pass    

def simulacion():
    global tiempo
    while not FinalizoSimulacion():
        AceptarProcesos(tiempo)
        EjecutarRafaga()
        tiempo += 1