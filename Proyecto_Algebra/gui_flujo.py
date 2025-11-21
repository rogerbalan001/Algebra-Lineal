import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import makarov as m  # Importamos tu módulo
import sys
import time

# Dependencias para la gráfica
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Clase para redirigir la salida de print() a un widget ---
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
        self.widget.config(state='disabled')

    def flush(self):
        pass

# --- NUEVA PANTALLA: Splash Screen (Animación de Inicio) ---
class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # --- Configuración de la Ventana ---
        # Ocultar bordes y barra de título
        self.overrideredirect(True)
        
        # Obtener tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Hacerla pantalla completa
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Fondo negro
        self.config(background="#1C1C1C")

        # --- Consola Falsa ---
        self.console_text = tk.Text(self, background="#1C1C1C", 
                                    foreground="#00FF7F", # Texto Verde
                                    font=('Consolas', 12),
                                    insertbackground="#00FF7F", # Cursor
                                    bd=0, # Sin borde
                                    padx=50, pady=50)
        self.console_text.pack(fill=tk.BOTH, expand=True)

        # --- Texto de la Animación ---
        self.boot_lines = [
            "Initializing system...",
            "Booting Markov Kernel v1.0...",
            "Connecting to local matrix processor...",
            "[ OK ] Connection established.",
            "Loading libraries:",
            "  > numpy.core.multiarray... loaded.",
            "  > matplotlib.pyplot... loaded.",
            "  > tkinter.ttk... loaded.",
            "Scanning for state definitions...",
            "Calculating probability space...",
            "Loading simulation components...",
            "  > Eigenvector calculation module... READY.",
            "  > N-step transition module... READY.",
            "  > Real-time plotter... READY.",
            "All systems operational.",
            "Starting Graphical User Interface...",
            "Welcome, operator."
        ]
        
        self.line_index = 0
        self.start_animation()

    def start_animation(self):
        """Inicia el proceso de 'escritura' línea por línea."""
        self.animate_line()

    def animate_line(self):
        if self.line_index < len(self.boot_lines):
            line = self.boot_lines[self.line_index]
            self.console_text.insert(tk.END, f"SYS_BOOT: {line}\n")
            self.console_text.see(tk.END)
            self.line_index += 1
            
            # Tiempo de espera aleatorio para un efecto más "real"
            delay = np.random.randint(50, 250)
            if self.line_index == len(self.boot_lines):
                delay = 1000 # Espera más larga en la última línea
            
            self.after(delay, self.animate_line)
        else:
            # Animación terminada
            self.launch_app()

    def launch_app(self):
        """Cierra la splash screen y muestra la app principal."""
        self.parent.deiconify() # Muestra la app principal
        self.destroy() # Destruye esta splash screen

# --- Aplicación Principal (Controlador de Vistas) ---
class MarkovApp(tk.Tk):
    """Controlador principal que maneja las 'pantallas' (Frames)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Simulador de Cadena de Markov (Flujo)")

        # --- Ventana más grande y centrada ---
        window_width = 1100
        window_height = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # --- ESTILOS Y COLORES (MODO OSCURO) ---
        
        # Paleta de Colores
        self.BG_COLOR = "#2E2E2E"
        self.FRAME_BG = "#3C3C3C"
        self.TEXT_COLOR = "#E0E0E0"
        self.WHITE = "#FFFFFF"
        self.BTN_BLUE = "#007BFF"
        self.BTN_BLUE_ACTIVE = "#0056b3"
        self.ENTRY_BG = "#5A5A5A"
        self.CONSOLE_BG = "#1C1C1C"
        self.CONSOLE_FG = "#00FF7F"

        style = ttk.Style(self)
        
        try:
            style.theme_use('clam') 
        except tk.TclError:
            pass 

        style.configure('.', 
            background=self.BG_COLOR, 
            foreground=self.TEXT_COLOR,
            font=('Calibri', 10)
        )
        style.configure('TFrame', background=self.BG_COLOR)
        style.configure('TLabelframe', 
            background=self.FRAME_BG, 
            labelmargins=10,
            font=('Calibri', 12)
        )
        style.configure('TLabelframe.Label', 
            background=self.FRAME_BG, 
            foreground=self.WHITE,
            font=('Calibri', 12, 'bold')
        )
        style.configure('TLabel', font=('Calibri', 11))
        style.map('TEntry',
            fieldbackground=[('!disabled', self.ENTRY_BG)],
            foreground=[('!disabled', self.WHITE)],
            insertcolor=[('!disabled', self.WHITE)]
        )
        style.configure('TEntry', font=('Calibri', 11))
        
        style.map('TCombobox',
            fieldbackground=[('!disabled', self.ENTRY_BG)],
            foreground=[('!disabled', self.WHITE)],
            selectbackground=[('!disabled', self.ENTRY_BG)],
            selectforeground=[('!disabled', self.WHITE)]
        )
        
        style.configure('TButton', 
            font=('Calibri', 11, 'bold'),
            background='#5A5A5A', 
            foreground=self.WHITE,
            padding=5
        )
        style.map('TButton',
            background=[('active', '#6A6A6A')],
            foreground=[('active', self.WHITE)]
        )
        style.configure('Accent.TButton', 
            background=self.BTN_BLUE,
            foreground=self.WHITE,
            font=('Calibri', 11, 'bold'),
            padding=5
        )
        style.map('Accent.TButton',
            background=[('active', self.BTN_BLUE_ACTIVE)],
            foreground=[('active', self.WHITE)]
        )
        # --- FIN DE ESTILOS ---

        # Contenedor principal para las "pantallas"
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Datos compartidos
        self.chain = None
        self.states = []
        self.frames = {}
        
        # Crear las dos "ventanas"
        for F in (ConfigScreen, ResultsScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ConfigScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

# --- Pantalla 1: Configuración de la Matriz ---
class ConfigScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.matrix_entries = []
        self.states_list = []
        
        content_frame = ttk.Frame(self, padding="30")
        content_frame.pack(expand=True) 

        config_frame = ttk.LabelFrame(content_frame, text="1. Definir Sistema")
        config_frame.pack(fill=tk.X, pady=10, ipady=10)

        states_frame = ttk.Frame(config_frame, padding=5)
        states_frame.pack(fill=tk.X)
        
        ttk.Label(states_frame, text="Estados (separados por coma):").pack(side=tk.LEFT, padx=5)
        self.states_entry = ttk.Entry(states_frame, width=40)
        self.states_entry.insert(0, "soleado, lluvioso")
        self.states_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.define_matrix_btn = ttk.Button(states_frame, text="Generar Matriz", command=self.on_define_matrix)
        self.define_matrix_btn.pack(side=tk.LEFT, padx=5)
        
        self.matrix_frame = ttk.LabelFrame(content_frame, text="2. Introducir Matriz de Transición")
        self.matrix_frame.pack(fill=tk.BOTH, expand=True, pady=10, ipady=10)

        self.continue_btn = ttk.Button(content_frame, 
                                       text="Validar y Ver Resultados >>", 
                                       command=self.on_validate_and_continue, 
                                       style='Accent.TButton')
        self.continue_btn.pack(pady=20, ipady=8) 

        self.on_define_matrix()

    def on_define_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.states_list = [s.strip() for s in self.states_entry.get().split(',') if s.strip()]
        n = len(self.states_list)
        
        if n == 0: return
        self.matrix_entries = []
        
        ttk.Label(self.matrix_frame, text="Desde ↓ / Hacia →", padding=5, font=('Calibri', 10, 'italic')).grid(row=0, column=0, sticky="e")
        for j, state in enumerate(self.states_list):
            ttk.Label(self.matrix_frame, text=state, anchor="center", padding=5, font=('Calibri', 10, 'bold')).grid(row=0, column=j + 1)

        for i, state in enumerate(self.states_list):
            ttk.Label(self.matrix_frame, text=f"{state}", padding=5, font=('Calibri', 10, 'bold')).grid(row=i + 1, column=0, sticky="e")
            row_entries = []
            for j in range(n):
                entry = ttk.Entry(self.matrix_frame, width=6, justify="center")
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
            
        if self.states_entry.get() == "soleado, lluvioso":
            self.matrix_entries[0][0].insert(0, "0.7")
            self.matrix_entries[0][1].insert(0, "0.3")
            self.matrix_entries[1][0].insert(0, "0.5")
            self.matrix_entries[1][1].insert(0, "0.5")

    def on_validate_and_continue(self):
        n = len(self.states_list)
        if n == 0:
            messagebox.showerror("Error", "Primero debe definir los estados.")
            return

        matrix = []
        try:
            for i in range(n):
                row = []
                for j in range(n):
                    val = float(self.matrix_entries[i][j].get())
                    row.append(val)
                matrix.append(row)
            
            original_stdout = sys.stdout
            sys.stdout = self.controller.frames[ResultsScreen].redirector
            
            self.controller.chain = m.MarkovChain(self.states_list, matrix)
            self.controller.states = self.states_list
            
            print("---")
            print("Cadena de Markov cargada y validada con éxito.")
            sys.stdout = original_stdout 

            self.controller.show_frame(ResultsScreen)

        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Valor inválido en la matriz: {e}")
        except Exception as e:
            messagebox.showerror("Error de Validación", f"Error al crear la cadena: {e}")
        finally:
            sys.stdout = original_stdout


# --- Pantalla 2: Resultados y Gráficas ---
class ResultsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.BG_COLOR = controller.BG_COLOR
        self.FRAME_BG = controller.FRAME_BG
        self.TEXT_COLOR = controller.TEXT_COLOR
        self.WHITE = controller.WHITE
        self.CONSOLE_BG = controller.CONSOLE_BG
        self.CONSOLE_FG = controller.CONSOLE_FG
        self.BTN_BLUE = controller.BTN_BLUE

        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)

        back_btn = ttk.Button(nav_frame, text="<< Volver (Meter otros valores)", command=lambda: controller.show_frame(ConfigScreen))
        back_btn.pack(side=tk.LEFT)

        exit_btn = ttk.Button(nav_frame, text="Salir de la Aplicación", command=self.controller.destroy)
        exit_btn.pack(side=tk.RIGHT)

        main_pane = ttk.PanedWindow(self, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        results_frame = ttk.LabelFrame(main_pane, text="Resultados", padding=10)
        main_pane.add(results_frame, weight=1)

        self.console_text = scrolledtext.ScrolledText(results_frame, height=10, state='disabled',
                                                      background=self.CONSOLE_BG,
                                                      foreground=self.CONSOLE_FG,
                                                      insertbackground=self.WHITE,
                                                      font=('Consolas', 10)
                                                      )
        self.console_text.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=5, pady=5)
        
        self.redirector = TextRedirector(self.console_text)

        action_frame = ttk.Frame(results_frame)
        action_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.steady_btn = ttk.Button(action_frame, text="Calcular Estado Estacionario", command=self.on_steady_state)
        self.steady_btn.pack(fill=tk.X, pady=3)

        multi_day_frame = ttk.Frame(action_frame)
        multi_day_frame.pack(fill=tk.X, pady=3)
        ttk.Label(multi_day_frame, text="Prob. a N días:").pack(side=tk.TOP)
        self.days_entry = ttk.Entry(multi_day_frame, width=5)
        self.days_entry.insert(0, "3")
        self.days_entry.pack(side=tk.LEFT, padx=5)
        self.multi_day_btn = ttk.Button(multi_day_frame, text="Calcular", command=self.on_multi_day)
        self.multi_day_btn.pack(side=tk.LEFT)

        plot_frame_container = ttk.LabelFrame(main_pane, text="Gráficas de Evolución (Simulación)", padding=10)
        main_pane.add(plot_frame_container, weight=3)

        plot_controls = ttk.Frame(plot_frame_container)
        plot_controls.pack(fill=tk.X, pady=5)

        ttk.Label(plot_controls, text="Estado Inicial:").pack(side=tk.LEFT)
        self.initial_state_combo = ttk.Combobox(plot_controls, width=12, state="readonly", font=('Calibri', 10))
        self.initial_state_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(plot_controls, text="Nº Pasos:").pack(side=tk.LEFT)
        self.sim_steps_entry = ttk.Entry(plot_controls, width=7)
        self.sim_steps_entry.insert(0, "100")
        self.sim_steps_entry.pack(side=tk.LEFT, padx=5)

        self.plot_btn = ttk.Button(plot_controls, text="Generar Gráfica de Evolución", 
                                     command=self.on_plot_evolution, 
                                     style='Accent.TButton')
        self.plot_btn.pack(side=tk.LEFT, padx=10, ipady=3)

        self.plot_canvas_frame = ttk.Frame(plot_frame_container)
        self.plot_canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    def on_show(self):
        if self.controller.states:
            self.initial_state_combo['values'] = self.controller.states
            self.initial_state_combo.current(0)
    
    def on_steady_state(self):
        if not self.controller.chain: return
        try:
            original_stdout = sys.stdout
            sys.stdout = self.redirector
            
            steady = self.controller.chain.find_steady_state()
            print("\n--- Estado Estacionario (Vector Propio) ---")
            for state, prob in zip(self.controller.states, steady):
                print(f"  {state}: {prob:.4f}")
            
            sys.stdout = original_stdout
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular: {e}")
        finally:
            sys.stdout = original_stdout

    def on_multi_day(self):
        if not self.controller.chain: return
        try:
            days = int(self.days_entry.get())
            if days <= 0: 
                messagebox.showwarning("Entrada Inválida", "Nro. de días debe ser positivo.")
                return

            original_stdout = sys.stdout
            sys.stdout = self.redirector

            p_n = self.controller.chain.multi_day_probabilities(days)
            print(f"\n--- Matriz de Probabilidades a {days} días (P^{days}) ---")
            print(p_n)
            
            sys.stdout = original_stdout
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular: {e}")
        finally:
            sys.stdout = original_stdout

    def on_plot_evolution(self):
        if not self.controller.chain:
            messagebox.showwarning("Error", "No hay cadena cargada.")
            return

        try:
            initial_state = self.initial_state_combo.current()
            steps = int(self.sim_steps_entry.get())
            if initial_state < 0 or steps <= 0:
                messagebox.showwarning("Entrada Inválida", "Seleccione estado inicial y Nro. de pasos válidos (positivos).")
                return
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Nro. de pasos debe ser un entero.")
            return
            
        for widget in self.plot_canvas_frame.winfo_children():
            widget.destroy()

        original_stdout = sys.stdout
        sys.stdout = self.redirector
        print(f"\n--- Generando Gráfica (Simulación de {steps} pasos) ---")
        sys.stdout = original_stdout

        try:
            history = self.controller.chain.simulate_steps(initial_state, steps)
            steady = self.controller.chain.find_steady_state()
            freqs = np.bincount(history, minlength=len(self.controller.states)) / len(history)

            fig = Figure(figsize=(6, 7), dpi=100, facecolor=self.BG_COLOR) 
            axes = fig.subplots(2, 1) 

            # Subplot 1
            ax1 = axes[0]
            ax1.set_facecolor(self.FRAME_BG) 
            ax1.plot(history, 'o-', alpha=0.7, markersize=4, color='#00A0FF') 
            ax1.set_yticks(range(len(self.controller.states)))
            ax1.set_yticklabels(self.controller.states, color=self.TEXT_COLOR)
            ax1.set_title(f'Evolución del Sistema ({steps} pasos)', color=self.WHITE)
            # ax1.set_xlabel('Tiempo', color=self.TEXT_COLOR) # Eliminado para evitar choque
            ax1.set_ylabel('Estado', color=self.TEXT_COLOR)
            ax1.grid(True, alpha=0.2, color=self.TEXT_COLOR)
            ax1.tick_params(colors=self.TEXT_COLOR, which='both')
            for spine in ax1.spines.values():
                spine.set_edgecolor(self.TEXT_COLOR)

            # Subplot 2
            ax2 = axes[1]
            ax2.set_facecolor(self.FRAME_BG) 
            x = np.arange(len(self.controller.states))
            width = 0.35
            ax2.bar(x - width / 2, steady, width, label='Teórico', alpha=0.8, color=self.BTN_BLUE) 
            ax2.bar(x + width / 2, freqs, width, label='Simulado', alpha=0.8, color='#FF5733') 
            ax2.set_xticks(x)
            ax2.set_xticklabels(self.controller.states, color=self.TEXT_COLOR)
            ax2.set_ylabel('Probabilidad', color=self.TEXT_COLOR)
            ax2.set_title('Estacionario: Teórico vs Simulado', color=self.WHITE) # Título acortado
            ax2.grid(True, alpha=0.2, color=self.TEXT_COLOR)
            legend = ax2.legend()
            legend.get_frame().set_facecolor(self.FRAME_BG)
            for text in legend.get_texts():
                text.set_color(self.TEXT_COLOR)
            ax2.tick_params(colors=self.TEXT_COLOR, which='both')
            for spine in ax2.spines.values():
                spine.set_edgecolor(self.TEXT_COLOR)
            
            fig.tight_layout(pad=3.0) 
            
            canvas = FigureCanvasTkAgg(fig, master=self.plot_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error al Graficar", f"No se pudo generar la gráfica.\n\nError: {e}\n\n(Asegúrate de que 'makarov.py' esté corregido)")
            print(f"\n--- ERROR AL GRAFICAR: {e} ---")


# --- Ejecutar la aplicación ---
if __name__ == "__main__":
    # --- MODIFICACIÓN PARA SPLASH SCREEN ---
    app = MarkovApp()
    app.withdraw() # Ocultar la ventana principal al inicio
    
    splash = SplashScreen(app) # Mostrar la pantalla de carga
    
    app.mainloop()