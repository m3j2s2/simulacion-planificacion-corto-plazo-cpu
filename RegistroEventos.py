class RegistroEventos:
    """Clase para registrar todos los eventos que ocurren durante la simulación"""
    
    def __init__(self):
        self.eventos = []
        self.datos_procesos = []  # Para almacenar los datos finales de cada proceso
        self.tiempo_ocioso_cpu = 0
        self.tiempo_retorno_tanda = 0
    
    def registrar_arribo_proceso(self, tiempo, nombre_proceso):
        """Registra cuando arriba un proceso (inicio del TIP)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'ARRIBO',
            'descripcion': f"Arriba el proceso {nombre_proceso} (inicio del TIP)"
        })
    
    def registrar_incorporacion_proceso(self, tiempo, nombre_proceso):
        """Registra cuando se incorpora un proceso al sistema (final del TIP)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'INCORPORACION',
            'descripcion': f"Se incorpora al sistema el proceso {nombre_proceso} finaliza su TIP"
        })
    
    def registrar_carga_proceso(self, tiempo, nombre_proceso):
        """Registra cuando se carga un proceso (inicio del TCP)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'CARGA',
            'descripcion': f"Se carga el proceso {nombre_proceso}"
        })
    
    def registrar_fin_carga_proceso(self, tiempo, nombre_proceso):
        """Registra cuando termina la carga de un proceso (final del TCP)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'FIN_CARGA',
            'descripcion': f"Termina la carga del proceso {nombre_proceso}"
        })
    
    def registrar_inicio_rafaga(self, tiempo, nombre_proceso):
        """Registra cuando un proceso ejecuta su ráfaga (inicio de la ráfaga)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'INICIO_RAFAGA',
            'descripcion': f"El proceso {nombre_proceso} ejecuta su ráfaga"
        })
    
    def registrar_fin_rafaga(self, tiempo, nombre_proceso):
        """Registra cuando finaliza la ráfaga de un proceso"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'FIN_RAFAGA',
            'descripcion': f"Finaliza la ráfaga del proceso {nombre_proceso}"
        })
    
    def registrar_corte_rafaga_quantum(self, tiempo, nombre_proceso):
        """Registra cuando se corta la ráfaga por quantum (Round Robin)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'CORTE_QUANTUM',
            'descripcion': f"Se corta la ráfaga del proceso {nombre_proceso} por quantum"
        })
    
    def registrar_corte_rafaga_prioridad(self, tiempo, nombre_proceso, nombre_proceso_prioridad):
        """Registra cuando se corta la ráfaga por llegada de proceso con mayor prioridad"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'CORTE_PRIORIDAD',
            'descripcion': f"Se corta la ráfaga del proceso {nombre_proceso} porque llegó un proceso con mayor prioridad ({nombre_proceso_prioridad})"
        })
    
    def registrar_corte_rafaga_srt(self, tiempo, nombre_proceso, nombre_proceso_corto):
        """Registra cuando se corta la ráfaga por llegada de proceso con menor ráfaga restante"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'CORTE_SRT',
            'descripcion': f"Se corta la ráfaga del proceso {nombre_proceso} porque llegó un proceso con menor ráfaga restante ({nombre_proceso_corto})"
        })
    
    def registrar_proceso_bloqueado(self, tiempo, nombre_proceso):
        """Registra cuando un proceso pasa a estado bloqueado (E/S)"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'BLOQUEADO',
            'descripcion': f"El proceso {nombre_proceso} pasa a estado bloqueado (E/S)"
        })
    
    def registrar_proceso_desbloqueado(self, tiempo, nombre_proceso):
        """Registra cuando un proceso sale del estado bloqueado"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'DESBLOQUEADO',
            'descripcion': f"El proceso {nombre_proceso} sale del estado bloqueado"
        })

    def registrar_proceso_empiza_TFP(self, tiempo, nombre_proceso):
        """Registra cuando un proceso empieza a finalizarse"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'FINALIZANDO',
            'descripcion': f"El proceso {nombre_proceso} termina su ultima rafaga, empieza su proceso de finalizacion"
        })
    
    def registrar_proceso_terminado(self, tiempo, nombre_proceso):
        """Registra cuando un proceso termina completamente"""
        self.eventos.append({
            'tiempo': tiempo,
            'tipo': 'TERMINADO',
            'descripcion': f"El proceso {nombre_proceso} termina su ejecución"
        })
    
    def Agregar_Tabla_Finalproceso(self, datos_proceso):
        """
        Agrega los datos finales de un proceso
        datos_proceso debe ser una tupla: (nombre, tiempo_retorno, tiempo_retorno_normalizado, tiempo_espera)
        """
        self.datos_procesos.append(datos_proceso)
    
    def establecer_tiempo_ocioso(self, tiempo_ocioso):
        """Establece el tiempo que la CPU estuvo ociosa"""
        self.tiempo_ocioso_cpu = tiempo_ocioso
    
    def calcular_tiempo_retorno_tanda(self):
        """
        Calcula el tiempo de retorno de la tanda
        Desde que se incorpora el primer proceso (fin de su TIP) hasta que termina el último (fin de su TFP)
        """
        if not self.eventos:
            return 0
        
        # esto es para buscar el primer evento de INCORPORACION (fin del primer TIP)
        tiempo_inicio = None
        for evento in self.eventos:
            if evento['tipo'] == 'INCORPORACION':
                tiempo_inicio = evento['tiempo']
                break
        
        # esto es para buscar el ultimo evento de TERMINADO (fin del último TFP)
        tiempo_fin = None
        for evento in reversed(self.eventos):
            if evento['tipo'] == 'TERMINADO':
                tiempo_fin = evento['tiempo']
                break
        
        if tiempo_inicio is not None and tiempo_fin is not None:
            self.tiempo_retorno_tanda = tiempo_fin - tiempo_inicio
        
        return self.tiempo_retorno_tanda
    
    def obtener_eventos_ordenados(self):
        """Retorna los eventos ordenados por tiempo"""
        return sorted(self.eventos, key=lambda x: x['tiempo'])
    
    def generar_archivo_texto(self, nombre_archivo):
        """Genera un archivo de texto con todos los eventos de la simulación y estadísticas finales"""
        eventos_ordenados = self.obtener_eventos_ordenados()
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write(" " * 35 + "REGISTRO DE EVENTOS DE SIMULACIÓN\n")
            f.write("=" * 100 + "\n\n")
            
            if not eventos_ordenados:
                f.write("No se registraron eventos durante la simulación.\n")
            else:
                for evento in eventos_ordenados:
                    tiempo = evento['tiempo']
                    descripcion = evento['descripcion']
                    f.write(f"Tiempo {tiempo:4d}: {descripcion}\n")
            
            f.write("\n" + "=" * 100 + "\n")
            f.write(f"Total de eventos registrados: {len(eventos_ordenados)}\n")
            f.write("=" * 100 + "\n\n")
            
            # Tabla de datos por proceso
            if self.datos_procesos:
                f.write("\n" + "=" * 100 + "\n")
                f.write(" " * 35 + "ESTADÍSTICAS POR PROCESO\n")
                f.write("=" * 100 + "\n\n")
                
                # esto seria para los nombres de las columnas de la tabla
                f.write(f"{'Proceso':<15} {'T. Retorno':<15} {'T. Ret. Norm.':<20} {'T. Espera':<15}\n")
                f.write("-" * 100 + "\n")
                
                # Datos de cada proceso
                suma_tr = 0
                suma_trn = 0
                suma_te = 0
                
                for nombre, t_retorno, t_retorno_norm, t_espera in self.datos_procesos:
                    f.write(f"{nombre:<15} {t_retorno:<15.2f} {t_retorno_norm:<20.4f} {t_espera:<15.2f}\n")
                    suma_tr += t_retorno
                    suma_trn += t_retorno_norm
                    suma_te += t_espera
                
                # los tiempos promedios
                n_procesos = len(self.datos_procesos)
                if n_procesos > 0:
                    f.write("-" * 100 + "\n")
                    f.write(f"{'PROMEDIO':<15} {suma_tr/n_procesos:<15.2f} {suma_trn/n_procesos:<20.4f} {suma_te/n_procesos:<15.2f}\n")
                
                f.write("=" * 100 + "\n")
            
            # esto es para la estadísticas de la tanda
            f.write("\n" + "=" * 100 + "\n")
            f.write(" " * 35 + "ESTADÍSTICAS DE LA TANDA\n")
            f.write("=" * 100 + "\n\n")
            
            # Calcula el tiempo de retorno de la tanda
            tiempo_retorno = self.calcular_tiempo_retorno_tanda()
            
            f.write(f"Tiempo de retorno de la tanda: {tiempo_retorno} unidades de tiempo\n")
            f.write(f"  (Desde la incorporación del primer proceso hasta la finalización del último)\n\n")
            
            f.write(f"Tiempo de CPU ociosa: {self.tiempo_ocioso_cpu} unidades de tiempo\n\n")
            
            # Tiempo medio de retorno de la tanda
            if self.datos_procesos:
                suma_retornos = sum(datos[1] for datos in self.datos_procesos)
                tiempo_medio_retorno = suma_retornos / len(self.datos_procesos)
                f.write(f"Tiempo medio de retorno: {tiempo_medio_retorno:.2f} unidades de tiempo\n")
            
            f.write("=" * 100 + "\n")
    
    def limpiar(self):
        self.eventos = []
        self.datos_procesos = []
        self.tiempo_ocioso_cpu = 0
        self.tiempo_retorno_tanda = 0