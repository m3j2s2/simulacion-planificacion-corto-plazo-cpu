import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path
from Procesos import Proceso
from graficador_gantt import GraficadorGantt
from cargador_politicas import CargarPoliticas

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
        self.processor = None  # Guardar referencia al procesador
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar tandas disponibles
        self.cargar_tandas_disponibles()
    
    def crear_interfaz(self):
        self._crear_titulo()
        self._crear_frame_tiempos()
        self._crear_frame_seleccion()
        self._crear_tabla_procesos()
        self._crear_boton_iniciar()
    
    def _crear_titulo(self):
        titulo = tk.Label(
            self.root,
            text="Simulación de Planificación de Procesador",
            font=("Arial", 20, "bold"),
            bg='#f0f0f0'
        )
        titulo.pack(pady=12)
    
    def _crear_frame_tiempos(self):
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
        
        campos = [
            ("TIP", self.tip_var, 0),
            ("TCP", self.tcp_var, 2),
            ("TFP", self.tfp_var, 4),
            ("Quantum", self.quantum_var, 6)
        ]
        
        for label, var, col in campos:
            tk.Label(tiempos_frame, text=label, bg='white').grid(
                row=0, column=col, padx=5, pady=5, sticky='w'
            )
            tk.Entry(tiempos_frame, textvariable=var, width=10).grid(
                row=0, column=col+1, padx=5, pady=5
            )
    
    def _crear_frame_seleccion(self):
        frame_seleccion = tk.Frame(self.root, bg='#f0f0f0')
        frame_seleccion.pack(padx=20, pady=6, fill='x')
        
        self._crear_frame_tanda(frame_seleccion)
        self._crear_frame_politica(frame_seleccion)
    
    def _crear_frame_tanda(self, parent):
        frame_tanda = tk.LabelFrame(
            parent,
            text="Seleccione una tanda de procesos",
            bg='white',
            padx=8,
            pady=8
        )
        frame_tanda.pack(side='left', padx=(0,10), fill='x', expand=True)
        
        tanda_content = tk.Frame(frame_tanda, bg='white')
        tanda_content.pack(fill='x')
        
        self.combo_tanda = ttk.Combobox(
            tanda_content,
            textvariable=self.tanda_var,
            state='readonly',
            width=35
        )
        self.combo_tanda.pack(side='left', padx=5, pady=5)
        
        btn_aceptar_tanda = tk.Button(
            tanda_content,
            text="Aceptar",
            command=self.cargar_procesos_desde_json,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 9, 'bold')
        )
        btn_aceptar_tanda.pack(side='left', padx=5, pady=5)
        
        btn_cargar = tk.Button(
            tanda_content,
            text="Cargar JSON",
            command=self.cargar_json_externo
        )
        btn_cargar.pack(side='left', padx=5, pady=5)
    
    def _crear_frame_politica(self, parent):
        frame_politica = tk.LabelFrame(
            parent,
            text="Política de Planificación",
            bg='white',
            padx=8,
            pady=8
        )
        frame_politica.pack(side='left', fill='x', expand=True)
        
        politicas = ["FCFS", "SJF", "Prioridad Preemtiva", "SRT", "Round Robin"]
        self.combo_politica = ttk.Combobox(
            frame_politica,
            textvariable=self.politica_var,
            values=politicas,
            state='readonly',
            width=30
        )
        self.combo_politica.pack(padx=5, pady=5)
    
    def _crear_tabla_procesos(self):
        frame_tabla = tk.LabelFrame(self.root, bg='white', padx=10, pady=10)
        frame_tabla.pack(padx=20, pady=8, fill='both', expand=True)
        
        columnas = (
            'Nombre',
            'Tiempo de Arribo',
            'Ráfaga CPU',
            'Cantidad Ráfagas',
            'Duración E/S',
            'Prioridad'
        )
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show='headings',
            height=12
        )
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor='center')
        
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient='vertical',
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _crear_boton_iniciar(self):
        botones_frame = tk.Frame(self.root, bg='#f0f0f0')
        botones_frame.pack(fill='x', padx=20, pady=10)
        
        btn_iniciar = tk.Button(
            botones_frame,
            text="Iniciar simulación",
            command=self.iniciar_simulacion,
            width=18,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold')
        )
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
            self.combo_tanda['values'] = []
    
    def cargar_procesos_desde_json(self, event=None):
        tanda_seleccionada = self.tanda_var.get()
        if not tanda_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una tanda de procesos")
            return
        ruta_json = Path("Tandas") / tanda_seleccionada
        self._cargar_json_desde_ruta(ruta_json)
    
    def cargar_json_externo(self):
        ruta_json = filedialog.askopenfilename(
            title="Seleccione un archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if ruta_json:
            self._cargar_json_desde_ruta(Path(ruta_json))
    
    def _cargar_json_desde_ruta(self, ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                self.procesos_data = json.load(f)
            
            self._actualizar_tabla()
            messagebox.showinfo("Éxito", f"Se cargaron {len(self.procesos_data)} procesos")
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: {ruta_json}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON no es válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def _actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Llenar tabla
        for proceso in self.procesos_data:
            self.tree.insert('', 'end', values=(
                proceso.get('nombre', ''),
                proceso.get('tiempo_arribo', ''),
                proceso.get('duracion_rafaga_cpu', ''),
                proceso.get('cantidad_rafagas_cpu', ''),
                proceso.get('duracion_rafaga_es', ''),
                proceso.get('prioridad_externa', '')
            ))
    
    def _crear_instancias_procesos(self):
        instancias = []
        for p in self.procesos_data:
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
        if not self._validar_datos():
            return
        
        # Obtener parámetros
        tip, tcp, tfp, quantum = self._obtener_parametros()
        if tip is None:
            return
        
        # Crear instancias de procesos
        cola_espera = self._crear_instancias_procesos()
        if not cola_espera:
            messagebox.showerror("Error", "No se pudieron convertir los procesos a instancias")
            return
        
        # Crear y ejecutar procesador
        self.processor = self._crear_procesador(tip, tcp, tfp, quantum, cola_espera)
        if self.processor is None:
            return
        
        if not self._ejecutar_simulacion(self.processor):
            return
        
        # Graficar resultados
        procesos_a_graficar = self._obtener_procesos_para_graficar(self.processor, cola_espera)
        if not procesos_a_graficar:
            messagebox.showinfo("Resultado", "La simulación terminó pero no hay eventos para graficar.")
            return
        
        self._graficar_resultados(procesos_a_graficar)
        
        # Preguntar si quiere guardar el archivo de eventos
        self._preguntar_guardar_eventos()
    
    def _preguntar_guardar_eventos(self):
        """Pregunta al usuario si desea guardar el archivo de eventos"""
        respuesta = messagebox.askyesno(
            "Simulación Finalizada",
            "La simulación ha finalizado correctamente.\n\n¿Desea guardar el registro de eventos?"
        )
        
        if respuesta:
            self._guardar_archivo_eventos()
    
    def _guardar_archivo_eventos(self):
        """Abre un diálogo para guardar el archivo de eventos"""
        if self.processor is None or not hasattr(self.processor, 'registro_eventos'):
            messagebox.showerror("Error", "No hay eventos para guardar")
            return
        
        # Obtener nombre de archivo sugerido
        politica = self.politica_var.get().replace(" ", "_")
        nombre_sugerido = f"eventos_simulacion_{politica}.txt"
        
        # Abrir diálogo para guardar archivo
        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar registro de eventos",
            initialfile=nombre_sugerido,
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if ruta_archivo:
            try:
                self.processor.registro_eventos.generar_archivo_texto(ruta_archivo)
                messagebox.showinfo(
                    "Éxito",
                    f"El registro de eventos se guardó exitosamente en:\n{ruta_archivo}"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo guardar el archivo:\n{str(e)}"
                )
    
    def _validar_datos(self):
        if not self.procesos_data:
            messagebox.showwarning("Advertencia", "Debe cargar una tanda de procesos")
            return False
        
        if not self.politica_var.get():
            messagebox.showwarning("Advertencia", "Debe seleccionar una política de planificación")
            return False
        
        return True
    
    def _obtener_parametros(self):
        try:
            tip = int(self.tip_var.get())
            tcp = int(self.tcp_var.get())
            tfp = int(self.tfp_var.get())
            quantum = int(self.quantum_var.get())
            return tip, tcp, tfp, quantum
        except ValueError:
            messagebox.showerror("Error", "Los tiempos deben ser números enteros")
            return None, None, None, None
    
    def _crear_procesador(self, tip, tcp, tfp, quantum, cola_espera):
        politica = self.politica_var.get()
        return CargarPoliticas.crear_procesador(
            politica, tip, tcp, tfp, quantum, cola_espera
        )
    
    def _ejecutar_simulacion(self, processor):
        try:
            processor.simulacion()
            return True
        except Exception as e:
            messagebox.showerror("Error en simulación", f"Ocurrió un error: {e}")
            return False
    
    def _obtener_procesos_para_graficar(self, processor, cola_espera):
        if hasattr(processor, "Cola_de_Terminado") and processor.Cola_de_Terminado:
            return processor.Cola_de_Terminado.copy()
        
        procesos_con_eventos = []
        for p in cola_espera:
            if hasattr(p, "Tuplas") and p.Tuplas:
                procesos_con_eventos.append(p)
        return procesos_con_eventos
    
    def _graficar_resultados(self, procesos):
        try:
            graficador = GraficadorGantt(self.root)
            graficador.graficar(procesos)
        except Exception as e:
            messagebox.showerror("Error gráfico", f"No se pudo generar la gráfica: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()