import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

# Importar tus clases de simulación
from Procesos import Proceso
try:
    from FCFS import FCFS
except Exception:
    FCFS = None

# Matplotlib para mostrar resultados
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Planificación")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.tip_var = tk.StringVar(value="2")
        self.tcp_var = tk.StringVar(value="2")
        self.tfp_var = tk.StringVar(value="2")
        self.quantum_var = tk.StringVar(value="4")
        self.tanda_var = tk.StringVar()
        self.politica_var = tk.StringVar()
        
        self.procesos_data = []
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar tandas disponibles
        self.cargar_tandas_disponibles()
    
    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(
            self.root,
            text="Simulación de Planificación de Procesador",
            font=("Arial", 20, "bold"),
            bg='#f0f0f0'
        )
        titulo.pack(pady=12)
        
        # Frame para tiempos
        frame_tiempos = tk.LabelFrame(
            self.root,
            text="Ingrese los tiempos:",
            font=("Arial", 10),
            bg='white',
            padx=10,
            pady=10
        )
        frame_tiempos.pack(padx=20, pady=6, fill='x')
        
        tiempos_frame = tk.Frame(frame_tiempos, bg='white')
        tiempos_frame.pack(fill='x')
        
        tk.Label(tiempos_frame, text="TIP", bg='white').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(tiempos_frame, textvariable=self.tip_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(tiempos_frame, text="TCP", bg='white').grid(row=0, column=2, padx=5, pady=5, sticky='w')
        tk.Entry(tiempos_frame, textvariable=self.tcp_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(tiempos_frame, text="TFP", bg='white').grid(row=0, column=4, padx=5, pady=5, sticky='w')
        tk.Entry(tiempos_frame, textvariable=self.tfp_var, width=10).grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(tiempos_frame, text="Quantum", bg='white').grid(row=0, column=6, padx=5, pady=5, sticky='w')
        tk.Entry(tiempos_frame, textvariable=self.quantum_var, width=10).grid(row=0, column=7, padx=5, pady=5)
        
        # Frame seleccion
        frame_seleccion = tk.Frame(self.root, bg='#f0f0f0')
        frame_seleccion.pack(padx=20, pady=6, fill='x')
        
        frame_tanda = tk.LabelFrame(frame_seleccion, text="Seleccione una tanda de procesos", bg='white', padx=8, pady=8)
        frame_tanda.pack(side='left', padx=(0,10), fill='x', expand=True)
        
        tanda_content = tk.Frame(frame_tanda, bg='white')
        tanda_content.pack(fill='x')
        
        self.combo_tanda = ttk.Combobox(tanda_content, textvariable=self.tanda_var, state='readonly', width=40)
        self.combo_tanda.pack(side='left', padx=5, pady=5)
        self.combo_tanda.bind('<<ComboboxSelected>>', self.cargar_procesos_desde_json)
        
        btn_cargar = tk.Button(tanda_content, text="Cargar Json", command=self.cargar_json)
        btn_cargar.pack(side='left', padx=5, pady=5)
        
        btn_crear = tk.Button(tanda_content, text="Crear Tanda", command=self.crear_tanda)
        btn_crear.pack(side='left', padx=5, pady=5)
        
        frame_politica = tk.LabelFrame(frame_seleccion, text="Política de Planificación", bg='white', padx=8, pady=8)
        frame_politica.pack(side='left', fill='x', expand=True)
        
        politicas = ["FCFS", "SJF", "Prioridad Preemtiva", "SRT", "Round Robin"]
        self.combo_politica = ttk.Combobox(frame_politica, textvariable=self.politica_var, values=politicas, state='readonly', width=30)
        self.combo_politica.pack(padx=5, pady=5)
        
        # Tabla de procesos
        frame_tabla = tk.LabelFrame(self.root, bg='white', padx=10, pady=10)
        frame_tabla.pack(padx=20, pady=8, fill='both', expand=True)
        
        columnas = ('Nombre', 'Tiempo de Arribo', 'Ráfaga CPU', 'Cantidad Ráfagas', 'Duración E/S', 'Prioridad')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=12)
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botones inferiores
        botones_frame = tk.Frame(self.root, bg='#f0f0f0')
        botones_frame.pack(fill='x', padx=20, pady=10)
        
        btn_mas_info = tk.Button(botones_frame, text="Más Información", command=self.mostrar_mas_info, width=18)
        btn_mas_info.pack(side='right', padx=6)
        
        btn_iniciar = tk.Button(botones_frame, text="Iniciar simulación", command=self.iniciar_simulacion, width=18, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        btn_iniciar.pack(side='right', padx=6)
    
    def cargar_tandas_disponibles(self):
        tandas_path = Path("Tandas")
        if tandas_path.exists() and tandas_path.is_dir():
            json_files = list(tandas_path.glob("*.json"))
            nombres = [f.name for f in json_files]
            self.combo_tanda['values'] = nombres
            if nombres:
                self.combo_tanda.current(0)
        else:
            # no existe carpeta, no mostrar error aún
            self.combo_tanda['values'] = []
    
    def cargar_procesos_desde_json(self, event=None):
        tanda_seleccionada = self.tanda_var.get()
        if not tanda_seleccionada:
            return
        ruta_json = Path("Tandas") / tanda_seleccionada
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                self.procesos_data = json.load(f)
            # limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            # llenar tabla
            for proceso in self.procesos_data:
                self.tree.insert('', 'end', values=(
                    proceso.get('nombre', ''),
                    proceso.get('tiempo_arribo', ''),
                    proceso.get('duracion_rafaga_cpu', ''),
                    proceso.get('cantidad_rafagas_cpu', ''),
                    proceso.get('duracion_rafaga_es', ''),
                    proceso.get('prioridad_externa', '')
                ))
            messagebox.showinfo("Éxito", f"Se cargaron {len(self.procesos_data)} procesos")
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: {ruta_json}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON no es válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def cargar_json(self):
        self.cargar_tandas_disponibles()
    
    def crear_tanda(self):
        messagebox.showinfo("Información", "Funcionalidad 'Crear Tanda' por implementar")
    
    def mostrar_mas_info(self):
        if not self.procesos_data:
            messagebox.showinfo("Información", "No hay procesos cargados")
            return
        info_window = tk.Toplevel(self.root)
        info_window.title("Información Detallada de Procesos")
        info_window.geometry("600x400")
        text_widget = tk.Text(info_window, wrap='word', padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        for proceso in self.procesos_data:
            text_widget.insert('end', f"Proceso: {proceso.get('nombre', 'N/A')}\n")
            text_widget.insert('end', f"  Tiempo de Arribo: {proceso.get('tiempo_arribo', 'N/A')}\n")
            text_widget.insert('end', f"  Cantidad de Ráfagas CPU: {proceso.get('cantidad_rafagas_cpu', 'N/A')}\n")
            text_widget.insert('end', f"  Duración Ráfaga CPU: {proceso.get('duracion_rafaga_cpu', 'N/A')}\n")
            text_widget.insert('end', f"  Duración E/S: {proceso.get('duracion_rafaga_es', 'N/A')}\n")
            text_widget.insert('end', f"  Prioridad Externa: {proceso.get('prioridad_externa', 'N/A')}\n")
            text_widget.insert('end', "-" * 50 + "\n\n")
        text_widget.config(state='disabled')
    
    def _crear_instancias_procesos(self):
        """Convierte self.procesos_data (diccionarios) a instancias de Proceso de tu módulo."""
        instancias = []
        for p in self.procesos_data:
            # mapear claves posibles del JSON a los nombres que espera tu clase Proceso
            nombre = p.get('nombre') or p.get('Nombre') or p.get('name') or f"P{len(instancias)+1}"
            tiempo_arribo = int(p.get('tiempo_arribo', p.get('tiempo_de_arribo', 0)))
            cantidad_rafagas = int(p.get('cantidad_rafagas_cpu', p.get('cantidad_de_rafagas', 1)))
            duracion_rafaga = int(p.get('duracion_rafaga_cpu', p.get('duracion_de_rafaga', 1)))
            duracion_es = int(p.get('duracion_rafaga_es', p.get('duracion_de_entrada_salida', 0)))
            prioridad = int(p.get('prioridad_externa', p.get('prioridad', 0)))
            proc = Proceso(
                nombre=nombre,
                tiempo_de_arribo=tiempo_arribo,
                cantidad_de_rafagas=cantidad_rafagas,
                duracion_de_rafaga=duracion_rafaga,
                duracion_de_entrada_salida=duracion_es,
                prioridad_externa=prioridad
            )
            instancias.append(proc)
        return instancias

    def iniciar_simulacion(self):
        # Validaciones
        if not self.procesos_data:
            messagebox.showwarning("Advertencia", "Debe cargar una tanda de procesos")
            return
        politica = self.politica_var.get()
        if not politica:
            messagebox.showwarning("Advertencia", "Debe seleccionar una política de planificación")
            return
        try:
            tip = int(self.tip_var.get())
            tcp = int(self.tcp_var.get())
            tfp = int(self.tfp_var.get())
            quantum = int(self.quantum_var.get())
        except ValueError:
            messagebox.showerror("Error", "Los tiempos deben ser números enteros")
            return
        
        # Crear instancias de Proceso
        cola_espera = self._crear_instancias_procesos()
        if not cola_espera:
            messagebox.showerror("Error", "No se pudieron convertir los procesos a instancias")
            return
        
        # Sólo FCFS está implementado en tus clases provistas
        if politica == "FCFS":
            if FCFS is None:
                messagebox.showerror("Error", "La clase FCFS no está disponible (archivo FCFS.py faltante o con errores).")
                return
            try:
                processor = FCFS(TIP=tip, TCP=tcp, TFP=tfp, Quantum=quantum, Cola_de_Espera=cola_espera)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el procesador: {e}")
                return
        else:
            messagebox.showinfo("No implementado", f"La política '{politica}' no está implementada en este demo.\nPor ahora solo FCFS está soportada.")
            return
        
        # Ejecutar simulación (bloqueante): corre tu método simulacion()
        try:
            processor.simulacion()
        except Exception as e:
            messagebox.showerror("Error en simulación", f"Ocurrió un error al ejecutar la simulación: {e}")
            return
        
        # Recolectar procesos terminados para graficar (y cualquier proceso con eventos)
        procesos_a_graficar = []
        # suelo tomar Cola_de_Terminado si existe, si no tomar la lista original
        if hasattr(processor, "Cola_de_Terminado") and processor.Cola_de_Terminado:
            procesos_a_graficar = processor.Cola_de_Terminado.copy()
        else:
            # tomar procesos que tengan tuplas (eventos)
            for p in cola_espera:
                if hasattr(p, "Tuplas") and p.Tuplas:
                    procesos_a_graficar.append(p)
            
        if not procesos_a_graficar:
            messagebox.showinfo("Resultado", "La simulación terminó pero no hay eventos para graficar.")
            return
        
        # Preparar Gantt con matplotlib
        try:
            self._graficar_gantt(procesos_a_graficar)
        except Exception as e:
            messagebox.showerror("Error gráfico", f"No se pudo generar la gráfica: {e}")
            return
        
        messagebox.showinfo("Simulación", "Simulación finalizada y resultados graficados.")
    
    def _graficar_gantt(self, procesos):
        """Dibuja un Gantt con scroll horizontal y vertical para diagramas largos."""
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        from matplotlib.figure import Figure
        
        # colores por tipo de evento
        colores = {
            'cpu': '#2ca02c',
            'Entrada/Salida': '#1f77b4',
            'tcp': '#ff7f0e',
            'tip': '#9467bd',
            'Finalizacion': '#d62728'
        }
        
        # Calcular tiempo máximo
        tiempo_maximo = 0
        for proc in procesos:
            tuplas = []
            if hasattr(proc, "verTuplas"):
                tuplas = proc.verTuplas()
            else:
                tuplas = getattr(proc, "Tuplas", [])
            for (inicio, duracion, tipo) in tuplas:
                tiempo_maximo = max(tiempo_maximo, inicio + duracion)
        
        # Crear ventana con scrollbars
        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("Diagrama de Gantt - Simulación")
        gantt_window.geometry("1400x800")
        
        # Frame principal con scrollbars
        main_frame = tk.Frame(gantt_window)
        main_frame.pack(fill='both', expand=True)
        
        # Canvas con scrollbars
        canvas_widget = tk.Canvas(main_frame, bg='white')
        canvas_widget.pack(side='left', fill='both', expand=True)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(main_frame, orient='vertical', command=canvas_widget.yview)
        scrollbar_y.pack(side='right', fill='y')
        
        scrollbar_x = ttk.Scrollbar(gantt_window, orient='horizontal', command=canvas_widget.xview)
        scrollbar_x.pack(side='bottom', fill='x')
        
        canvas_widget.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        
        # Frame interno para matplotlib
        inner_frame = tk.Frame(canvas_widget, bg='white')
        canvas_widget.create_window((0, 0), window=inner_frame, anchor='nw')
        
        # Calcular dimensiones de la figura (más generoso con el espacio)
        # Ancho: 0.5 pulgadas por unidad de tiempo (evita amontonamiento)
        ancho_fig = max(15, tiempo_maximo * 0.5)
        # Alto: 1 pulgada por proceso
        alto_fig = max(8, len(procesos) * 1.0)
        
        # Crear figura de matplotlib
        fig = Figure(figsize=(ancho_fig, alto_fig), dpi=100)
        ax = fig.add_subplot(111)
        
        yticks = []
        ylabels = []
        for idx, proc in enumerate(procesos):
            tuplas = []
            if hasattr(proc, "verTuplas"):
                tuplas = proc.verTuplas()
            else:
                tuplas = getattr(proc, "Tuplas", [])
            
            y = len(procesos) - idx
            yticks.append(y)
            nombre = getattr(proc, "nombre", None) or getattr(proc, "get_Nombre", lambda: f"P{idx+1}")()
            ylabels.append(nombre)
            
            for (inicio, duracion, tipo) in tuplas:
                if duracion <= 0:
                    continue
                color = colores.get(tipo, '#7f7f7f')
                ax.barh(y, duracion, left=inicio, height=0.6, align='center',
                       edgecolor='black', alpha=0.9, color=color, linewidth=1.5)
                
                if duracion >= 1.5:
                    ax.text(inicio + duracion/2, y, tipo, va='center', ha='center',
                           color='white', fontsize=9, fontweight='bold')
        
        # Configurar ejes
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels, fontsize=10)
        ax.set_xlabel("Tiempo", fontsize=12, fontweight='bold')
        ax.set_ylabel("Procesos", fontsize=12, fontweight='bold')
        ax.set_title("Diagrama de Gantt - Resultados de la Simulación",
                    fontsize=14, fontweight='bold', pad=20)
        
        # Ticks del eje X de 1 en 1 con mejor espaciado
        ax.set_xticks(range(0, int(tiempo_maximo) + 2, 1))
        ax.set_xlim(-0.5, tiempo_maximo + 1)
        ax.set_ylim(0.5, len(procesos) + 0.5)
        
        # Rotar etiquetas del eje X para mejor legibilidad
        ax.tick_params(axis='x', labelsize=9, rotation=0)
        
        # Grid
        ax.grid(axis='x', linestyle='--', linewidth=0.6, alpha=0.7, color='gray')
        ax.grid(axis='y', linestyle=':', linewidth=0.4, alpha=0.5, color='gray')
        ax.set_facecolor('#f9f9f9')
        
        # Leyenda
        patches = [mpatches.Patch(color=c, label=k) for k, c in colores.items()]
        ax.legend(handles=patches, loc='upper right', fontsize=10,
                 framealpha=0.95, edgecolor='black', fancybox=True)
        
        fig.tight_layout()
        
        # Integrar matplotlib en tkinter
        canvas_mpl = FigureCanvasTkAgg(fig, master=inner_frame)
        canvas_mpl.draw()
        canvas_mpl.get_tk_widget().pack()
        
        # Toolbar de navegación
        toolbar_frame = tk.Frame(gantt_window)
        toolbar_frame.pack(side='bottom', fill='x')
        toolbar = NavigationToolbar2Tk(canvas_mpl, toolbar_frame)
        toolbar.update()
        
        # Actualizar región scrollable
        inner_frame.update_idletasks()
        canvas_widget.config(scrollregion=canvas_widget.bbox('all'))
        
        # Bind mouse wheel para scroll
        def _on_mousewheel(event):
            canvas_widget.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_shift_mousewheel(event):
            canvas_widget.xview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_widget.bind_all("<MouseWheel>", _on_mousewheel)
        canvas_widget.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)
        
        # Limpiar bindings al cerrar ventana
        def on_closing():
            canvas_widget.unbind_all("<MouseWheel>")
            canvas_widget.unbind_all("<Shift-MouseWheel>")
            gantt_window.destroy()
        
        gantt_window.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()