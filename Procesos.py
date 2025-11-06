class Proceso:
    def __init__(self, nombre: str, tiempo_de_arribo: int, cantidad_de_rafagas: int,
                 duracion_de_rafaga: int, duracion_de_entrada_salida: int, prioridad_externa: int) -> None:

        for valor, nombre_campo in [
            (tiempo_de_arribo, "tiempo_de_arribo"),
            (cantidad_de_rafagas, "cantidad_de_rafagas"),
            (duracion_de_rafaga, "duracion_de_rafaga"),
            (duracion_de_entrada_salida, "duracion_de_entrada_salida"),
            (prioridad_externa, "prioridad_externa")
        ]:
            if not (isinstance(valor, (int)) and valor >= 0):
                raise ValueError(f"'{nombre_campo}' debe ser un número positivo.")
        
        
        self.nombre = nombre
        self.tiempo_de_arribo = tiempo_de_arribo
        self.cantidad_de_rafagas = cantidad_de_rafagas
        self.duracion_de_rafaga = duracion_de_rafaga
        self.duracion_de_entrada_salida = duracion_de_entrada_salida
        self.prioridad_externa = prioridad_externa
        ###datos de lo que seria la "pcb"
        self.duracion_de_entrada_salida_restante = duracion_de_entrada_salida
        self.Tiempo_de_Rafaga_Restante = duracion_de_rafaga
        self.Rafagas_restantes = cantidad_de_rafagas
        self.Tiempo_de_Inicio = 0
        self.tiempo_de_retorno = 0
        self.tiempo_de_retorno_normalizado = 0
        self.Tuplas = []

    def get_Nombre(self):
        return self.nombre  
    def get_Tiempo_de_Arribo(self): 
        return self.tiempo_de_arribo
    def get_Cantidad_de_Rafagas(self):
        return self.cantidad_de_rafagas
    def get_Duracion_de_Rafaga(self):
        return self.duracion_de_rafaga
    def get_Duracion_de_Entrada_Salida(self):
        return self.duracion_de_entrada_salida
    def get_Prioridad_Externa(self):
        return self.prioridad_externa
    
    def set_Tiempo_de_Retorno(self,tiempo: int):
        self.tiempo_de_retorno = tiempo - self.Tiempo_de_Inicio

    def get_Tiempo_de_Retorno(self):
        return self.tiempo_de_retorno

    def get_tiempo_de_retorno_normalizado(self):
        if self.Tiempo_de_Inicio != 0 and self.tiempo_de_retorno != 0 : 
            return self.tiempo_de_retorno/(self.duracion_de_rafaga*self.cantidad_de_rafagas)
        else: 
            return -1

    def Consumir_Rafaga(self):
        if self.Tiempo_de_Rafaga_Restante > 0:
            self.Tiempo_de_Rafaga_Restante -= 1

    def get_Tiempo_de_Rafaga_Restante(self):
        return self.Tiempo_de_Rafaga_Restante
    
    def reset_Tiempo_de_Rafaga_Restante(self):
        self.Tiempo_de_Rafaga_Restante = self.duracion_de_rafaga

    

    def Reducir_Rafagas_restantes(self):
        self.Rafagas_restantes -= 1

    def get_Rafagas_restantes(self):
        return self.Rafagas_restantes

    def set_Tiempo_de_inicio(self, tiempo:int ):
        self.Tiempo_de_inicio = tiempo

    def get_Tiempo_de_Inicio(self):
        return self.Tiempo_de_inicio

    def registrar_evento(self, inicio: int, duracion: int, tipo: str):
        self.Tuplas.append((inicio, duracion, tipo))

    def verTuplas(self):
        return self.Tuplas       
    
    def reducir_Tiempo_de_Entrada_Salida_Restante(self):
        self.duracion_de_entrada_salida_restante -= 1

    def reset_Tiempo_de_Entrada_Salida_Restante(self):
        self.duracion_de_entrada_salida_restante = self.duracion_de_entrada_salida

    def get_Duracion_de_Entrada_Salida_Restante(self):
        return self.duracion_de_entrada_salida_restante

    def __repr__(self) -> str:
        return (f"Proceso({self.nombre}, Arribo={self.tiempo_de_arribo}, "
                f"Ráfagas={self.cantidad_de_rafagas}, "
                f"DuraciónRáfaga={self.duracion_de_rafaga}, "
                f"E/S={self.duracion_de_entrada_salida}, "
                f"Prioridad={self.prioridad_externa})")
    
