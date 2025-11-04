import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # type: ignore
from matplotlib.figure import Figure
import matplotlib.patches as mpatches


class GraficadorGantt:
    """Clase encargada de generar y mostrar el diagrama de Gantt"""
    
    COLORES = {
        'cpu': '#2ca02c',
        'Entrada/Salida': '#1f77b4',
        'tcp': '#ff7f0e',
        'tip': '#9467bd',
        'Finalizacion': '#d62728'
    }
    
    def __init__(self, root):
        self.root = root
    
    def graficar(self, procesos):
        """Dibuja un Gantt con scroll horizontal y vertical"""
        tiempo_maximo = self._calcular_tiempo_maximo(procesos)
        gantt_window = self._crear_ventana()
        
        # Crear estructura de la ventana
        main_frame, canvas_widget, scrollbar_x, scrollbar_y = self._crear_estructura_scroll(gantt_window)
        
        # Frame interno para matplotlib
        inner_frame = tk.Frame(canvas_widget, bg='white')
        canvas_widget.create_window((0, 0), window=inner_frame, anchor='nw')
        
        # Crear y configurar figura
        fig, ax = self._crear_figura(procesos, tiempo_maximo)
        self._dibujar_procesos(ax, procesos)
        self._configurar_ejes(ax, procesos, tiempo_maximo)
        self._agregar_leyenda(ax)
        fig.tight_layout()
        
        # Integrar matplotlib en tkinter
        canvas_mpl = self._integrar_matplotlib(fig, inner_frame)
        self._crear_toolbar(gantt_window, canvas_mpl)
        
        # Configurar scroll
        self._configurar_scroll(canvas_widget, inner_frame, gantt_window)
    
    def _calcular_tiempo_maximo(self, procesos):
        tiempo_maximo = 0
        for proc in procesos:
            tuplas = self._obtener_tuplas(proc)
            for (inicio, duracion, tipo) in tuplas:
                tiempo_maximo = max(tiempo_maximo, inicio + duracion)
        return tiempo_maximo
    
    def _obtener_tuplas(self, proc):
        if hasattr(proc, "verTuplas"):
            return proc.verTuplas()
        return getattr(proc, "Tuplas", [])
    
    def _crear_ventana(self):
        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("Diagrama de Gantt - Simulación")
        gantt_window.geometry("1400x800")
        return gantt_window
    
    def _crear_estructura_scroll(self, gantt_window):
        main_frame = tk.Frame(gantt_window)
        main_frame.pack(fill='both', expand=True)
        
        canvas_widget = tk.Canvas(main_frame, bg='white')
        canvas_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar_y = ttk.Scrollbar(main_frame, orient='vertical', command=canvas_widget.yview)
        scrollbar_y.pack(side='right', fill='y')
        
        scrollbar_x = ttk.Scrollbar(gantt_window, orient='horizontal', command=canvas_widget.xview)
        scrollbar_x.pack(side='bottom', fill='x')
        
        canvas_widget.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        
        return main_frame, canvas_widget, scrollbar_x, scrollbar_y
    
    def _crear_figura(self, procesos, tiempo_maximo):
        ancho_fig = max(15, tiempo_maximo * 0.5)
        alto_fig = max(8, len(procesos) * 1.0)
        
        fig = Figure(figsize=(ancho_fig, alto_fig), dpi=100)
        ax = fig.add_subplot(111)
        return fig, ax
    
    def _dibujar_procesos(self, ax, procesos):
        for idx, proc in enumerate(procesos):
            tuplas = self._obtener_tuplas(proc)
            y = len(procesos) - idx
            
            for (inicio, duracion, tipo) in tuplas:
                if duracion <= 0:
                    continue
                
                color = self.COLORES.get(tipo, '#7f7f7f')
                ax.barh(y, duracion, left=inicio, height=0.6, align='center',
                       edgecolor='black', alpha=0.9, color=color, linewidth=1.5)
                
                if duracion >= 1.5:
                    ax.text(inicio + duracion/2, y, tipo, va='center', ha='center',
                           color='white', fontsize=9, fontweight='bold')
    
    def _configurar_ejes(self, ax, procesos, tiempo_maximo):
        yticks = []
        ylabels = []
        
        for idx, proc in enumerate(procesos):
            y = len(procesos) - idx
            yticks.append(y)
            nombre = getattr(proc, "nombre", None) or getattr(proc, "get_Nombre", lambda: f"P{idx+1}")()
            ylabels.append(nombre)
        
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels, fontsize=10)
        ax.set_xlabel("Tiempo", fontsize=12, fontweight='bold')
        ax.set_ylabel("Procesos", fontsize=12, fontweight='bold')
        ax.set_title("Diagrama de Gantt - Resultados de la Simulación",
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.set_xticks(range(0, int(tiempo_maximo) + 2, 1))
        ax.set_xlim(-0.5, tiempo_maximo + 1)
        ax.set_ylim(0.5, len(procesos) + 0.5)
        
        ax.tick_params(axis='x', labelsize=9, rotation=0)
        
        # Grid
        ax.grid(axis='x', linestyle='--', linewidth=0.6, alpha=0.7, color='gray')
        ax.grid(axis='y', linestyle=':', linewidth=0.4, alpha=0.5, color='gray')
        ax.set_facecolor('#f9f9f9')
    
    def _agregar_leyenda(self, ax):
        patches = [mpatches.Patch(color=c, label=k) for k, c in self.COLORES.items()]
        ax.legend(handles=patches, loc='upper right', fontsize=10,
                 framealpha=0.95, edgecolor='black', fancybox=True)
    
    def _integrar_matplotlib(self, fig, inner_frame):
        canvas_mpl = FigureCanvasTkAgg(fig, master=inner_frame)
        canvas_mpl.draw()
        canvas_mpl.get_tk_widget().pack()
        return canvas_mpl
    
    def _crear_toolbar(self, gantt_window, canvas_mpl):
        toolbar_frame = tk.Frame(gantt_window)
        toolbar_frame.pack(side='bottom', fill='x')
        toolbar = NavigationToolbar2Tk(canvas_mpl, toolbar_frame)
        toolbar.update()
    
    def _configurar_scroll(self, canvas_widget, inner_frame, gantt_window):
        inner_frame.update_idletasks()
        canvas_widget.config(scrollregion=canvas_widget.bbox('all'))
        
        def _on_mousewheel(event):
            canvas_widget.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_shift_mousewheel(event):
            canvas_widget.xview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_widget.bind_all("<MouseWheel>", _on_mousewheel)
        canvas_widget.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)
        
        def on_closing():
            canvas_widget.unbind_all("<MouseWheel>")
            canvas_widget.unbind_all("<Shift-MouseWheel>")
            gantt_window.destroy()
        
        gantt_window.protocol("WM_DELETE_WINDOW", on_closing)