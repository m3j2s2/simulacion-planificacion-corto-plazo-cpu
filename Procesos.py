class Procesos:
    def __init__(self, nombre: str, tiempo_de_arribo: float, cantidad_de_rafagas: int,
                 duracion_de_rafaga: float, duracion_de_entrada_salida: float, prioridad_externa: int) -> None:
        
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser una cadena (str).")
        
        for valor, nombre_campo in [
            (tiempo_de_arribo, "tiempo_de_arribo"),
            (cantidad_de_rafagas, "cantidad_de_rafagas"),
            (duracion_de_rafaga, "duracion_de_rafaga"),
            (duracion_de_entrada_salida, "duracion_de_entrada_salida"),
            (prioridad_externa, "prioridad_externa")
        ]:
            if not (isinstance(valor, (int, float)) and valor > 0):
                raise ValueError(f"'{nombre_campo}' debe ser un número positivo.")
        
        
        self.nombre = nombre
        self.tiempo_de_arribo = tiempo_de_arribo
        self.cantidad_de_rafagas = cantidad_de_rafagas
        self.duracion_de_rafaga = duracion_de_rafaga
        self.duracion_de_entrada_salida = duracion_de_entrada_salida
        self.prioridad_externa = prioridad_externa

    def __repr__(self) -> str:
        return (f"Proceso({self.nombre}, Arribo={self.tiempo_de_arribo}, "
                f"Ráfagas={self.cantidad_de_rafagas}, "
                f"DuraciónRáfaga={self.duracion_de_rafaga}, "
                f"E/S={self.duracion_de_entrada_salida}, "
                f"Prioridad={self.prioridad_externa})")