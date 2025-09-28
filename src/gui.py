"""
Interfaz Gráfica SIGET
Interfaz moderna y sofisticada para visualizar el sistema de tráfico urbano
Implementa animaciones y visualización en tiempo real
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math
import logging
from src.config import *

class ModernTrafficLightWidget:
    """Widget personalizado para representar un semáforo con animaciones"""
    
    def __init__(self, parent, light_id, intersection_name, x, y):
        self.parent = parent
        self.light_id = light_id
        self.intersection_name = intersection_name
        self.x = x
        self.y = y
        
        # Estado del semáforo
        self.current_state = 'RED'
        self.animation_frame = 0
        self.animation_direction = 1
        
        # Crear canvas para el semáforo
        self.canvas = tk.Canvas(
            parent,
            width=80,
            height=200,
            bg=COLORS['surface'],
            highlightthickness=2,
            highlightbackground=COLORS['primary']
        )
        self.canvas.place(x=x, y=y)
        
        # Dibujar estructura del semáforo
        self.draw_traffic_light_structure()
        
        # Iniciar animación
        self.animate()
    
    def draw_traffic_light_structure(self):
        """Dibuja la estructura base del semáforo"""
        # Marco del semáforo
        self.canvas.create_rectangle(
            10, 10, 70, 190,
            fill=COLORS['surface'],
            outline=COLORS['text_primary'],
            width=2
        )
        
        # Luces (inicialmente apagadas)
        self.red_light = self.canvas.create_oval(20, 20, 60, 60, fill=COLORS['gray_light'], outline='')
        self.yellow_light = self.canvas.create_oval(20, 80, 60, 120, fill=COLORS['gray_light'], outline='')
        self.green_light = self.canvas.create_oval(20, 140, 60, 180, fill=COLORS['gray_light'], outline='')
        
        # Etiqueta del semáforo
        self.canvas.create_text(
            40, 195,
            text=f"ID: {self.light_id}",
            fill=COLORS['text_secondary'],
            font=('Arial', 8, 'bold')
        )
    
    def update_state(self, new_state):
        """Actualiza el estado del semáforo con animación"""
        if self.current_state != new_state:
            self.current_state = new_state
            self.animate_state_change()
    
    def animate_state_change(self):
        """Anima el cambio de estado del semáforo"""
        # Efecto de parpadeo durante el cambio
        for i in range(6):
            self.parent.after(i * 100, self.toggle_lights)
    
    def toggle_lights(self):
        """Alterna las luces para efecto de parpadeo"""
        if self.animation_frame % 2 == 0:
            self.draw_lights(self.current_state)
        else:
            self.draw_lights('OFF')
        self.animation_frame += 1
    
    def draw_lights(self, state):
        """Dibuja las luces según el estado actual"""
        # Apagar todas las luces
        self.canvas.itemconfig(self.red_light, fill=COLORS['gray_light'])
        self.canvas.itemconfig(self.yellow_light, fill=COLORS['gray_light'])
        self.canvas.itemconfig(self.green_light, fill=COLORS['gray_light'])
        
        # Encender la luz correspondiente
        if state == 'RED':
            self.canvas.itemconfig(self.red_light, fill=COLORS['red_light'])
        elif state == 'YELLOW':
            self.canvas.itemconfig(self.yellow_light, fill=COLORS['yellow_light'])
        elif state == 'GREEN':
            self.canvas.itemconfig(self.green_light, fill=COLORS['green_light'])
    
    def animate(self):
        """Animación continua del semáforo"""
        # Efecto de brillo sutil
        if self.current_state != 'OFF':
            alpha = 0.7 + 0.3 * math.sin(time.time() * 2)
            self.canvas.configure(highlightbackground=self.get_highlight_color(alpha))
        
        # Programar siguiente frame
        self.parent.after(50, self.animate)

    def get_highlight_color(self, alpha):
        """Obtiene color de resaltado con transparencia"""
        if self.current_state == 'RED':
            return self.blend_colors(COLORS['red_light'], COLORS['primary'], alpha)
        elif self.current_state == 'YELLOW':
            return self.blend_colors(COLORS['yellow_light'], COLORS['primary'], alpha)
        elif self.current_state == 'GREEN':
            return self.blend_colors(COLORS['green_light'], COLORS['primary'], alpha)
        return COLORS['primary']
    
    def blend_colors(self, color1, color2, ratio):
        """Mezcla dos colores con una proporción dada"""
        # Implementación simplificada de mezcla de colores
        return color1  # Por simplicidad, retornamos el color principal

class SIGETGUI:
    """Interfaz principal del sistema SIGET"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.traffic_lights = {}
        self.server = None
        self.running = False
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        # Configurar logging para la GUI (después de crear widgets)
        self.setup_logging()
        
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("SIGET - Sistema de Gestión de Tráfico Urbano")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(True, True)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configura estilos modernos para la interfaz"""
        style = ttk.Style()
        
        # Configurar tema oscuro
        style.theme_use('clam')
        
        # Configurar colores para widgets
        style.configure('Title.TLabel',
                       background=COLORS['background'],
                       foreground=COLORS['text_primary'],
                       font=('Arial', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=COLORS['background'],
                       foreground=COLORS['text_secondary'],
                       font=('Arial', 12))
        
        style.configure('Modern.TButton',
                       background=COLORS['primary'],
                       foreground=COLORS['text_primary'],
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Danger.TButton',
                       background=COLORS['error'],
                       foreground=COLORS['text_primary'],
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Success.TButton',
                       background=COLORS['success'],
                       foreground=COLORS['text_primary'],
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Título principal
        title_label = ttk.Label(
            self.root,
            text="SIGET - Sistema de Gestión de Tráfico Urbano",
            style='Title.TLabel'
        )
        title_label.pack(pady=10)
        
        # Subtítulo
        subtitle_label = ttk.Label(
            self.root,
            text="Sistema Distribuido con Concurrencia y Sincronización",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Panel de control
        self.create_control_panel()
        
        # Panel de visualización
        self.create_visualization_panel()
        
        # Panel de logs
        self.create_log_panel()
        
        # Panel de estadísticas
        self.create_stats_panel()
    
    def create_control_panel(self):
        """Crea el panel de control del sistema"""
        control_frame = tk.Frame(self.root, bg=COLORS['surface'], relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Título del panel
        control_title = tk.Label(
            control_frame,
            text="Panel de Control",
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            font=('Arial', 12, 'bold')
        )
        control_title.pack(pady=5)
        
        # Botones de control
        button_frame = tk.Frame(control_frame, bg=COLORS['surface'])
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="Iniciar Sistema",
            command=self.start_system,
            style='Success.TButton'
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Detener Sistema",
            command=self.stop_system,
            style='Danger.TButton'
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.emergency_button = ttk.Button(
            button_frame,
            text="Modo Emergencia",
            command=self.trigger_emergency,
            style='Danger.TButton'
        )
        self.emergency_button.pack(side=tk.LEFT, padx=5)
        
        self.sync_button = ttk.Button(
            button_frame,
            text="Sincronizar",
            command=self.trigger_sync,
            style='Modern.TButton'
        )
        self.sync_button.pack(side=tk.LEFT, padx=5)
    
    def create_visualization_panel(self):
        """Crea el panel de visualización de semáforos"""
        viz_frame = tk.Frame(self.root, bg=COLORS['background'])
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Título del panel
        viz_title = tk.Label(
            viz_frame,
            text="Visualización de Semáforos",
            bg=COLORS['background'],
            fg=COLORS['text_primary'],
            font=('Arial', 12, 'bold')
        )
        viz_title.pack(pady=5)
        
        # Canvas para semáforos
        self.canvas = tk.Canvas(
            viz_frame,
            bg=COLORS['background'],
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crear semáforos de ejemplo
        self.create_sample_traffic_lights()
    
    def create_sample_traffic_lights(self):
        """Crea semáforos de ejemplo para visualización"""
        intersections = [
            ("Centro", 50, 50),
            ("Norte", 200, 50),
            ("Sur", 50, 300),
            ("Este", 200, 300),
            ("Oeste", 350, 50),
            ("Noroeste", 350, 300)
        ]
        
        for i, (name, x, y) in enumerate(intersections):
            light_id = f"TL{i+1:03d}"
            traffic_light = ModernTrafficLightWidget(self.canvas, light_id, name, x, y)
            self.traffic_lights[light_id] = traffic_light
    
    def create_log_panel(self):
        """Crea el panel de logs del sistema"""
        log_frame = tk.Frame(self.root, bg=COLORS['surface'], relief=tk.RAISED, bd=2)
        log_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Título del panel
        log_title = tk.Label(
            log_frame,
            text="Logs del Sistema",
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            font=('Arial', 12, 'bold')
        )
        log_title.pack(pady=5)
        
        # Área de texto para logs
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg=COLORS['background'],
            fg=COLORS['text_primary'],
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.X, padx=10, pady=5)
        
        # Scrollbar para logs
        log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
    
    def create_stats_panel(self):
        """Crea el panel de estadísticas del sistema"""
        stats_frame = tk.Frame(self.root, bg=COLORS['surface'], relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Título del panel
        stats_title = tk.Label(
            stats_frame,
            text="Estadísticas del Sistema",
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            font=('Arial', 12, 'bold')
        )
        stats_title.pack(pady=5)
        
        # Frame para estadísticas
        stats_content = tk.Frame(stats_frame, bg=COLORS['surface'])
        stats_content.pack(fill=tk.X, padx=10, pady=5)
        
        # Labels para estadísticas
        self.stats_labels = {}
        stats_info = [
            ("clientes_conectados", "Clientes Conectados: 0"),
            ("mensajes_procesados", "Mensajes Procesados: 0"),
            ("sincronizaciones", "Sincronizaciones: 0"),
            ("modo_emergencia", "Modo Emergencia: No")
        ]
        
        for i, (key, text) in enumerate(stats_info):
            label = tk.Label(
                stats_content,
                text=text,
                bg=COLORS['surface'],
                fg=COLORS['text_secondary'],
                font=('Arial', 10)
            )
            label.grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=2)
            self.stats_labels[key] = label
    
    def setup_logging(self):
        """Configura el sistema de logging para la GUI"""
        # Crear handler personalizado para mostrar logs en la GUI
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
        
        # Configurar logging
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format=LOG_FORMAT,
            handlers=[
                GUILogHandler(self.log_text),
                logging.FileHandler('siget.log')
            ]
        )
    
    def start_system(self):
        """Inicia el sistema SIGET"""
        if self.running:
            self.log_message("El sistema ya está ejecutándose")
            return
        
        try:
            # Limpiar semáforos anteriores si existen
            if self.traffic_lights:
                self.log_message("Limpiando semáforos anteriores...")
                for light_id, traffic_light in list(self.traffic_lights.items()):
                    try:
                        if hasattr(traffic_light, 'stop'):
                            traffic_light.stop()
                    except:
                        pass
                self.traffic_lights.clear()
            
            # Importar e iniciar servidor
            from src.traffic_server import TrafficServer
            self.server = TrafficServer()
            
            # Iniciar servidor en hilo separado
            server_thread = threading.Thread(target=self.server.start_server, daemon=True)
            server_thread.start()
            
            # Esperar un momento para que el servidor se inicie
            time.sleep(2)
            
            # Iniciar semáforos
            self.start_traffic_lights()
            
            # Esperar un momento para que los semáforos se conecten
            time.sleep(2)
            
            self.running = True
            self.log_message("Sistema SIGET iniciado correctamente")
            
            # Iniciar actualización de interfaz
            self.update_interface()
            
        except Exception as e:
            self.log_message(f"Error iniciando sistema: {e}")
            messagebox.showerror("Error", f"No se pudo iniciar el sistema: {e}")
    
    def start_traffic_lights(self):
        """Inicia los semáforos del sistema"""
        from src.traffic_light import TrafficLight
        
        intersections = [
            ("Centro", 50, 50),
            ("Norte", 200, 50),
            ("Sur", 50, 300),
            ("Este", 200, 300),
            ("Oeste", 350, 50),
            ("Noroeste", 350, 300)
        ]
        
        self.log_message("Iniciando semáforos...")
        
        for i, (name, x, y) in enumerate(intersections):
            light_id = f"TL{i+1:03d}"
            self.log_message(f"Creando semáforo {light_id} en {name}")
            
            traffic_light = TrafficLight(light_id, name, x, y)
            
            # Iniciar semáforo en hilo separado
            light_thread = threading.Thread(target=traffic_light.start, daemon=True)
            light_thread.start()
            
            # Guardar referencia
            self.traffic_lights[light_id] = traffic_light
            
            # Pequeña pausa entre semáforos para evitar problemas de conexión
            time.sleep(0.5)
        
        self.log_message(f"Se crearon {len(self.traffic_lights)} semáforos")
    
    def stop_system(self):
        """Detiene el sistema SIGET"""
        if not self.running:
            self.log_message("El sistema ya está detenido")
            return
        
        try:
            self.log_message("Deteniendo sistema SIGET...")
            
            # Marcar como detenido inmediatamente para evitar múltiples llamadas
            self.running = False
            
            # Detener semáforos de forma asíncrona
            def stop_traffic_lights():
                try:
                    for light_id, traffic_light in list(self.traffic_lights.items()):
                        try:
                            if hasattr(traffic_light, 'stop'):
                                traffic_light.stop()
                            self.log_message(f"Semáforo {light_id} detenido")
                        except Exception as e:
                            self.log_message(f"Error deteniendo semáforo {light_id}: {e}")
                    
                    # Limpiar diccionario de semáforos
                    self.traffic_lights.clear()
                    
                    # Detener servidor
                    if self.server:
                        self.server.stop_server()
                        self.server = None
                    
                    self.log_message("✅ Sistema SIGET detenido correctamente")
                    
                except Exception as e:
                    self.log_message(f"❌ Error deteniendo sistema: {e}")
            
            # Ejecutar en hilo separado para no bloquear la UI
            stop_thread = threading.Thread(target=stop_traffic_lights, daemon=True)
            stop_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Error deteniendo sistema: {e}")
            self.running = False
    
    def trigger_emergency(self):
        """Activa el modo de emergencia"""
        if not self.running or not self.server:
            messagebox.showwarning("Advertencia", "El sistema no está ejecutándose")
            return
        
        try:
            self.server.emergency_override()
            self.log_message("MODO DE EMERGENCIA ACTIVADO")
        except Exception as e:
            self.log_message(f"Error activando emergencia: {e}")
    
    def trigger_sync(self):
        """Activa sincronización manual"""
        if not self.running or not self.server:
            messagebox.showwarning("Advertencia", "El sistema no está ejecutándose")
            return
        
        try:
            self.server.trigger_synchronization()
            self.log_message("Sincronización manual activada")
        except Exception as e:
            self.log_message(f"Error en sincronización: {e}")
    
    def update_interface(self):
        """Actualiza la interfaz en tiempo real"""
        if not self.running:
            return
        
        try:
            # Actualizar estado de semáforos
            if self.server:
                status = self.server.get_system_status()
                
                # Actualizar estadísticas
                self.stats_labels['clientes_conectados'].config(
                    text=f"Clientes Conectados: {status['total_clients']}"
                )
                self.stats_labels['mensajes_procesados'].config(
                    text=f"Mensajes Procesados: {status['stats']['messages_processed']}"
                )
                self.stats_labels['sincronizaciones'].config(
                    text=f"Sincronizaciones: {status['stats']['sync_operations']}"
                )
                self.stats_labels['modo_emergencia'].config(
                    text=f"Modo Emergencia: {'Sí' if status['system_state']['emergency_mode'] else 'No'}"
                )
                
                # Actualizar estados de semáforos
                for client_id, client_info in status['clients'].items():
                    if client_id in self.traffic_lights:
                        self.traffic_lights[client_id].update_state(client_info['state'])
                
                # Debug: Mostrar información de semáforos locales
                if len(self.traffic_lights) > 0:
                    active_lights = 0
                    for light_id, traffic_light in self.traffic_lights.items():
                        if hasattr(traffic_light, 'running') and traffic_light.running:
                            active_lights += 1
                    
                    # Solo mostrar debug ocasionalmente para no saturar los logs
                    if hasattr(self, '_debug_counter'):
                        self._debug_counter += 1
                    else:
                        self._debug_counter = 0
                    
                    if self._debug_counter % 50 == 0:  # Cada 5 segundos aproximadamente
                        self.log_message(f"Debug: {active_lights}/{len(self.traffic_lights)} semáforos activos localmente")
        
        except Exception as e:
            self.log_message(f"Error actualizando interfaz: {e}")
        
        # Programar siguiente actualización
        self.root.after(UPDATE_INTERVAL, self.update_interface)
    
    def log_message(self, message):
        """Agrega un mensaje al log de la interfaz"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_text.insert(tk.END, log_entry + '\n')
        self.log_text.see(tk.END)
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if self.running:
            self.stop_system()
        self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal para ejecutar la GUI"""
    app = SIGETGUI()
    app.run()

if __name__ == "__main__":
    main()
