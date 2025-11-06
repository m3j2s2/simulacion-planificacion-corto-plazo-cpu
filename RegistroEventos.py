class RegistroEventos:
    """Clase para registrar todos los eventos que ocurren durante la simulación"""
    
    def __init__(self):
        self.eventos = []
    
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
        """Registra cuando un proceso empieza a finalizarse """
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
    
    def obtener_eventos_ordenados(self):
        """Retorna los eventos ordenados por tiempo"""
        return sorted(self.eventos, key=lambda x: x['tiempo'])
    
    def generar_archivo_texto(self, nombre_archivo):
        """Genera un archivo de texto con todos los eventos de la simulación"""
        eventos_ordenados = self.obtener_eventos_ordenados()
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(" " * 20 + "REGISTRO DE EVENTOS DE SIMULACIÓN\n")
            f.write("=" * 80 + "\n\n")
            
            if not eventos_ordenados:
                f.write("No se registraron eventos durante la simulación.\n")
                return
            
            for evento in eventos_ordenados:
                tiempo = evento['tiempo']
                descripcion = evento['descripcion']
                f.write(f"Tiempo {tiempo:4d}: {descripcion}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Total de eventos registrados: {len(eventos_ordenados)}\n")
            f.write("=" * 80 + "\n")
    
    def limpiar(self):
        """Limpia todos los eventos registrados"""
        self.eventos = []