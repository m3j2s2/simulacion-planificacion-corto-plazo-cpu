import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Procesos import Proceso
from FCFS import FCFS


class SimuladorPlanificacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificación de Procesador")
        self.root.geometry("1200x750")p
        self.root.configure(bg="#2b2b2b")
        
        self.procesos = []
        self.contador_procesos = 1
        self.simulador = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Label(main_frame, text="Simulador de Planificación de Procesador", 
                         font=("Arial", 20, "bold"), bg="#2b2b2b", fg="#ffffff")
        titulo.pack(pady=10)
        
        # Frame de configuración del procesador
        frame_config = tk.LabelFrame(main_frame, text="Configuración del Procesador", 
                                      font=("Arial", 12, "bold"), bg="#3b3b3b", 
                                      fg="#ffffff", padx=10, pady=10)
        frame_config.pack(fill=tk.X, padx=5, pady=5)
        
        # Campos de configuración del procesador
        tk.Label(frame_config, text="TIP:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.entry_tip = tk.Entry(frame_config, width=10)
        self.entry_tip.insert(0, "1")
        self.entry_tip.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_config, text="TCP:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        self.entry_tcp = tk.Entry(frame_config, width=10)
        self.entry_tcp.insert(0, "1")
        self.entry_tcp.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_config, text="TFP:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=4, padx=5, pady=5)
        self.entry_tfp = tk.Entry(frame_config, width=10)
        self.entry_tfp.insert(0, "1")
        self.entry_tfp.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(frame_config, text="Quantum:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=6, padx=5, pady=5)
        self.entry_quantum = tk.Entry(frame_config, width=10)
        self.entry_quantum.insert(0, "3")
        self.entry_quantum.grid(row=0, column=7, padx=5, pady=5)
        
        # Frame de entrada de procesos
        frame_entrada = tk.LabelFrame(main_frame, text="Agregar Proceso", 
                                      font=("Arial", 12, "bold"), bg="#3b3b3b", 
                                      fg="#ffffff", padx=10, pady=10)
        frame_entrada.pack(fill=tk.X, padx=5, pady=5)
        
        # Campos de entrada de procesos
        tk.Label(frame_entrada, text="Nombre:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(frame_entrada, width=12)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="T. Arribo:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_arribo = tk.Entry(frame_entrada, width=10)
        self.entry_arribo.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="Cant. Ráfagas:", bg="#3b3b3b", fg="#ffffff").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_cant_rafagas = tk.Entry(frame_entrada, width=10)
        self.entry_cant_rafagas.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="Dur. Ráfaga:", bg="#3b3b3b", fg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_dur_rafaga = tk.Entry(frame_entrada, width=12)
        self.entry_dur_rafaga.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="Dur. E/S:", bg="#3b3b3b", fg="#ffffff").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_dur_es = tk.Entry(frame_entrada, width=10)
        self.entry_dur_es.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(frame_entrada, text="Prioridad:", bg="#3b3b3b", fg="#ffffff").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.entry_prioridad = tk.Entry(frame_entrada, width=10)
        self.entry_prioridad.grid(row=1, column=5, padx=5, pady=5)
        
        # Botones de acción
        btn_frame = tk.Frame(frame_entrada, bg="#3b3b3b")
        btn_frame.grid(row=0, column=6, rowspan=2, padx=10, pady=5)
        
        btn_agregar = tk.Button(btn_frame, text="Agregar Proceso", 
                               command=self.agregar_proceso, bg="#4CAF50", 
                               fg="white", font=("Arial", 10, "bold"), width=15)
        btn_agregar.pack(pady=3)
        
        btn_simular = tk.Button(btn_frame, text="Simular FCFS", 
                               command=self.simular_fcfs, bg="#2196F3", 
                               fg="white", font=("Arial", 10, "bold"), width=15)
        btn_simular.pack(pady=3)
        
        btn_limpiar = tk.Button(btn_frame, text="Limpiar Todo", 
                               command=self.limpiar_todo, bg="#f44336", 
                               fg="white", font=("Arial", 10, "bold"), width=15)
        btn_limpiar.pack(pady=3)
        
        # Frame para la tabla de procesos
        frame_tabla = tk.LabelFrame(main_frame, text="Lista de Procesos", 
                                    font=("Arial", 12, "bold"), bg="#3b3b3b", 
                                    fg="#ffffff", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabla de procesos
        columnas = ("Nombre", "Arribo", "Cant. Ráfagas", "Dur. Ráfaga", "Dur. E/S", "Prioridad")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
        
        anchos = [100, 80, 110, 100, 90, 90]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        
        # Frame para resultados
        frame_resultados = tk.LabelFrame(main_frame, text="Resultados de la Simulación", 
                                        font=("Arial", 12, "bold"), bg="#3b3b3b", 
                                        fg="#ffffff", padx=10, pady=10)
        frame_resultados.pack(fill=tk.X, padx=5, pady=5)
        
        self.label_resultados = tk.Label(frame_resultados, text="Ejecute la simulación para ver los resultados", 
                                         bg="#3b3b3b", fg="#ffffff", font=("Arial", 10), 
                                         justify=tk.LEFT)
        self.label_resultados.pack(pady=5)
    
    def agregar_proceso(self):
        try:
            nombre = self.entry_nombre.get().strip()
            if not nombre:
                nombre = f"P{self.contador_procesos}"
            
            arribo = float(self.entry_arribo.get())
            cant_rafagas = int(self.entry_cant_rafagas.get())
            dur_rafaga = float(self.entry_dur_rafaga.get())
            dur_es = float(self.entry_dur_es.get())
            prioridad = int(self.entry_prioridad.get())
            
            proceso = Proceso(nombre, arribo, cant_rafagas, dur_rafaga, dur_es, prioridad)
            self.procesos.append(proceso)
            self.contador_procesos += 1
            
            # Limpiar campos
            self.entry_nombre.delete(0, tk.END)
            self.entry_arribo.delete(0, tk.END)
            self.entry_cant_rafagas.delete(0, tk.END)
            self.entry_dur_rafaga.delete(0, tk.END)
            self.entry_dur_es.delete(0, tk.END)
            self.entry_prioridad.delete(0, tk.END)
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            messagebox.showinfo("Éxito", f"Proceso '{nombre}' agregado correctamente")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los valores ingresados:\n{str(e)}")
        except TypeError as e:
            messagebox.showerror("Error", f"Error de tipo:\n{str(e)}")
    
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar procesos
        for p in self.procesos:
            valores = (p.get_Nombre(), p.get_Tiempo_de_Arribo(), 
                      p.get_Cantidad_de_Rafagas(), p.get_Duracion_de_Rafaga(),
                      p.get_Duracion_de_Entrada_Salida(), p.get_Prioridad_Externa())
            self.tree.insert("", tk.END, values=valores)
    
    def simular_fcfs(self):
        if not self.procesos:
            messagebox.showwarning("Advertencia", "Agregue al menos un proceso")
            return
        
        try:
            tip = int(self.entry_tip.get())
            tcp = int(self.entry_tcp.get())
            tfp = int(self.entry_tfp.get())
            quantum = int(self.entry_quantum.get())
            
            # Crear simulador FCFS
            self.simulador = FCFS(tip, tcp, tfp, quantum, self.procesos.copy())
            
            # Ejecutar simulación
            self.simulador.simulacion()
            
            # Mostrar resultados
            self.mostrar_resultados()
            
            # Mostrar diagrama de Gantt
            self.mostrar_gantt()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la configuración del procesador:\n{str(e)}")
    
    def mostrar_resultados(self):
        if not self.simulador:
            return
        
        procesos_terminados = self.simulador.Cola_de_Terminado
        tiempo_total = self.simulador.tiempo
        
        resultado = f"Tiempo total de simulación: {tiempo_total} unidades\n"
        resultado += f"Procesos terminados: {len(procesos_terminados)}\n\n"
        
        for proceso in procesos_terminados:
            resultado += f"--- {proceso.get_Nombre()} ---\n"
            tuplas = proceso.verTuplas()
            for inicio, duracion, tipo in tuplas:
                resultado += f"  {tipo}: inicio={inicio}, duración={duracion}\n"
        
        self.label_resultados.config(text=resultado)
    
    def mostrar_gantt(self):
        if not self.simulador:
            return
        
        # Crear ventana para el gráfico
        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("Diagrama de Gantt - FCFS")
        gantt_window.geometry("1000x600")
        gantt_window.configure(bg="#2b2b2b")
        
        fig = Figure(figsize=(12, 6), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#1e1e1e')
        
        colores = {
            'cpu': '#4CAF50',
            'tcp': '#FFC107',
            'tip': '#2196F3',
            'Entrada/Salida': '#FF5722',
            'Finalizacion': '#9C27B0'
        }
        
        procesos_terminados = self.simulador.Cola_de_Terminado
        
        # Dibujar eventos de cada proceso
        for i, proceso in enumerate(procesos_terminados):
            tuplas = proceso.verTuplas()
            for inicio, duracion, tipo in tuplas:
                color = colores.get(tipo, '#757575')
                ax.barh(i, duracion, left=inicio, color=color, 
                       edgecolor='white', linewidth=1, height=0.6)
                
                # Agregar etiqueta si el evento es suficientemente largo
                if duracion > 1:
                    ax.text(inicio + duracion/2, i, f"{tipo}\n{duracion}", 
                           ha='center', va='center', color='white', 
                           fontsize=8, fontweight='bold')
        
        # Configurar ejes
        ax.set_yticks(range(len(procesos_terminados)))
        ax.set_yticklabels([p.get_Nombre() for p in procesos_terminados])
        ax.set_xlabel('Tiempo', color='white', fontsize=12)
        ax.set_ylabel('Procesos', color='white', fontsize=12)
        ax.set_title('Diagrama de Gantt - Algoritmo FCFS', color='white', fontsize=14, fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=tipo) 
                          for tipo, color in colores.items()]
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor='#3b3b3b', edgecolor='white', labelcolor='white')
        
        fig.tight_layout()
        
        # Integrar gráfico en la ventana
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def limpiar_todo(self):
        self.procesos = []
        self.contador_procesos = 1
        self.simulador = None
        self.actualizar_tabla()
        self.label_resultados.config(text="Ejecute la simulación para ver los resultados")
        messagebox.showinfo("Limpieza", "Todos los datos han sido eliminados")


def iniciar_aplicacion():
    root = tk.Tk()
    app = SimuladorPlanificacion(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()