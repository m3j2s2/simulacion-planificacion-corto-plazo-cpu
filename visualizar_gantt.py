import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import json
from Procesos import Proceso
from FCFS import FCFS

class SimuladorPrueba:
    def __init__(self, ruta_json=None):
        self.ruta_json = ruta_json or "Tandas/procesos_tanda_5p.json"
        self.procesos = []
        self.simulador = None
        self.procesos_terminados = []
        
    def cargar_procesos(self):
        """Carga los procesos desde el archivo JSON especificado"""
        with open(self.ruta_json, "r") as archivo:
            data = json.load(archivo)

        for p in data:
            duracion_es = p["duracion_rafaga_es"]
            
            # Evitar error por valores de E/S iguales a 0
            proceso = Proceso(
                nombre=p["nombre"],
                tiempo_de_arribo=p["tiempo_arribo"],
                cantidad_de_rafagas=p["cantidad_rafagas_cpu"],
                duracion_de_rafaga=p["duracion_rafaga_cpu"],
                duracion_de_entrada_salida=duracion_es,
                prioridad_externa=p["prioridad_externa"]
            )
            self.procesos.append(proceso)
        return self.procesos

    def crear_diagrama_gantt(self):
        """Crea y muestra el diagrama de Gantt con los procesos terminados"""
        if not self.procesos_terminados:
            print("No hay procesos terminados para mostrar")
            return None
            
        # Crear la figura y los ejes
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.set_facecolor('#f0f0f0')
        fig.patch.set_facecolor('white')
        
        # Definir colores para cada tipo de evento
        colores = {
            'cpu': '#4CAF50',      # Verde
            'tcp': '#FFC107',      # Amarillo
            'tip': '#2196F3',      # Azul
            'Entrada/Salida': '#FF5722',  # Naranja
            'Finalizacion': '#9C27B0'     # Púrpura
        }
        
        # Agregar una leyenda para los tipos de eventos
        legend_elements = [Rectangle((0,0),1,1, facecolor=color, label=tipo) 
                          for tipo, color in colores.items()]
        
        self.procesos_terminados.sort(key=lambda p: p.get_Tiempo_de_Arribo(),reverse=True)
        for i, proceso in enumerate(self.procesos_terminados):
            tuplas = proceso.verTuplas()
            for inicio, duracion, tipo in tuplas:
                color = colores.get(tipo, '#757575')  # Gris por defecto si no se encuentra el tipo
                ax.barh(i, duracion, left=inicio, color=color, 
                       edgecolor='white', linewidth=1, height=0.6)
                
                # Agregar etiqueta si el evento es suficientemente largo
                if duracion > 1:
                    ax.text(inicio + duracion/2, i, f"{tipo}\n{duracion}", 
                           ha='center', va='center',
                           color='black' if tipo == 'tcp' else 'white',
                           fontsize=8, fontweight='bold')
        
        # Configurar ejes y etiquetas
        ax.set_yticks(range(len(self.procesos_terminados)))
        ax.set_yticklabels([p.get_Nombre() for p in self.procesos_terminados])
        ax.set_xlabel('Tiempo', fontsize=12)
        ax.set_ylabel('Procesos', fontsize=12)
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
        # Agregar título y leyenda
        plt.title('Diagrama de Gantt - Planificación de Procesos', pad=20, fontsize=14)
        ax.legend(handles=legend_elements, loc='upper center', 
                 bbox_to_anchor=(0.5, -0.1), ncol=5)
        
        # Ajustar el layout para que quepa todo
        # Calcular tiempo máximo para definir los ticks del eje X
        tiempo_maximo = max(
            inicio + duracion 
            for proceso in self.procesos_terminados 
            for inicio, duracion, tipo in proceso.verTuplas()
        )

        # Configurar ticks del eje X de 1 en 1
        ax.set_xticks(range(0, int(tiempo_maximo) + 2, 1))

        plt.tight_layout()
        return fig

    def ejecutar_simulacion(self, tip=2, tcp=2, tfp=2, quantum=4):
        """Ejecuta la simulación FCFS con los parámetros especificados"""
        # Cargar procesos si no se han cargado
        if not self.procesos:
            self.cargar_procesos()
        
        # Crear y ejecutar el simulador
        self.simulador = FCFS(TIP=tip, TCP=tcp, TFP=tfp, Quantum=quantum, Cola_de_Espera=self.procesos)
        self.simulador.simulacion()
        
        # Guardar los procesos terminados
        self.procesos_terminados = self.simulador.Cola_de_Terminado
        
        # Mostrar información básica de la simulación
        print(f"Simulación completada:")
        print(f"Tiempo total: {self.simulador.tiempo}")
        print(f"Procesos terminados: {len(self.procesos_terminados)}")
        
    def mostrar_resultados(self):
        """Muestra el diagrama de Gantt y los resultados de la simulación"""
        if not self.procesos_terminados:
            print("No hay resultados para mostrar. Ejecute la simulación primero.")
            return
        
        # Crear y mostrar el diagrama de Gantt
        fig = self.crear_diagrama_gantt()
        if fig:
            plt.show()
            
        # Mostrar resumen detallado de cada proceso
        print("\nResumen detallado de procesos:")
        for proceso in self.procesos_terminados:
            print(f"\n--- {proceso.get_Nombre()} ---")
            for inicio, duracion, tipo in proceso.verTuplas():
                print(f"  {tipo}: inicio={inicio}, duración={duracion}")

# Ejemplo de uso:
simulador = SimuladorPrueba("Tandas/procesos_tanda_5p.json")
simulador.ejecutar_simulacion()
simulador.mostrar_resultados()