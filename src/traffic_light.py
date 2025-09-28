"""
Semáforo Inteligente - Cliente del sistema SIGET
Implementa un semáforo con estados y comunicación con el servidor central
"""

import socket
import threading
import time
import json
import logging
from enum import Enum
from src.config import *

class TrafficLightState(Enum):
    """Estados posibles del semáforo"""
    RED = 0
    YELLOW = 1
    GREEN = 2

class TrafficLight:
    """
    Semáforo inteligente que se comunica con el servidor central
    Implementa concurrencia y sincronización para evitar condiciones de carrera
    """
    
    def __init__(self, light_id, intersection_name, position_x, position_y):
        self.light_id = light_id
        self.intersection_name = intersection_name
        self.position_x = position_x
        self.position_y = position_y
        
        # Estado del semáforo
        self.current_state = TrafficLightState.RED
        self.previous_state = TrafficLightState.RED
        
        # Sincronización
        self.state_lock = threading.Lock()  # Mutex para proteger el estado
        self.communication_lock = threading.Lock()  # Mutex para comunicación
        self.sync_semaphore = threading.Semaphore(1)  # Semáforo para sincronización
        
        # Comunicación
        self.socket = None
        self.connected = False
        self.server_address = (SERVER_HOST, SERVER_PORT)
        
        # Control de concurrencia
        self.running = False
        self.threads = []
        
        # Logging
        self.logger = logging.getLogger(f'TrafficLight-{light_id}')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Estadísticas
        self.state_changes = 0
        self.last_sync_time = time.time()
        
    def connect_to_server(self):
        """Establece conexión con el servidor central"""
        try:
            with self.communication_lock:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(5)
                self.socket.connect(self.server_address)
                self.connected = True
                self.logger.info(f"Conectado al servidor central en {self.server_address}")
                return True
        except Exception as e:
            self.logger.error(f"Error conectando al servidor: {e}")
            return False
    
    def disconnect_from_server(self):
        """Cierra la conexión con el servidor"""
        try:
            with self.communication_lock:
                if self.socket:
                    self.socket.close()
                    self.connected = False
                    self.logger.info("Desconectado del servidor central")
        except Exception as e:
            self.logger.error(f"Error desconectando: {e}")
    
    def send_state_to_server(self, state, timestamp):
        """Envía el estado actual al servidor central de forma thread-safe"""
        if not self.connected:
            return False
            
        try:
            with self.communication_lock:
                message = {
                    'type': 'state_update',
                    'light_id': self.light_id,
                    'intersection': self.intersection_name,
                    'state': state.name,
                    'timestamp': timestamp,
                    'position': (self.position_x, self.position_y)
                }
                
                data = json.dumps(message).encode('utf-8')
                self.socket.send(data)
                self.logger.debug(f"Estado enviado al servidor: {state.name}")
                return True
        except Exception as e:
            self.logger.error(f"Error enviando estado: {e}")
            return False
    
    def receive_command_from_server(self):
        """Recibe comandos del servidor central"""
        try:
            with self.communication_lock:
                if not self.connected:
                    return None
                    
                self.socket.settimeout(1)
                data = self.socket.recv(1024)
                if data:
                    message = json.loads(data.decode('utf-8'))
                    self.logger.debug(f"Comando recibido: {message}")
                    return message
        except socket.timeout:
            pass
        except Exception as e:
            self.logger.error(f"Error recibiendo comando: {e}")
        return None
    
    def change_state(self, new_state):
        """Cambia el estado del semáforo de forma thread-safe"""
        with self.state_lock:
            if self.current_state != new_state:
                self.previous_state = self.current_state
                self.current_state = new_state
                self.state_changes += 1
                timestamp = time.time()
                
                self.logger.info(f"Estado cambiado: {self.previous_state.name} -> {self.current_state.name}")
                
                # Enviar estado al servidor
                self.send_state_to_server(new_state, timestamp)
                
                return True
        return False
    
    def get_state_duration(self, state):
        """Obtiene la duración de un estado específico"""
        return STATE_DURATIONS.get(state.name, 5)
    
    def traffic_light_cycle(self):
        """Ciclo principal del semáforo - ejecutado en hilo separado"""
        self.logger.info("Iniciando ciclo del semáforo")
        
        while self.running:
            try:
                # Verificar comando del servidor
                command = self.receive_command_from_server()
                if command and command.get('type') == 'emergency_override':
                    self.handle_emergency_override(command)
                    continue
                
                # Ciclo normal de estados
                for state in [TrafficLightState.RED, TrafficLightState.GREEN, TrafficLightState.YELLOW]:
                    if not self.running:
                        break
                        
                    # Adquirir semáforo para sincronización
                    with self.sync_semaphore:
                        self.change_state(state)
                        duration = self.get_state_duration(state)
                        
                        # Esperar con posibilidad de interrupción
                        for _ in range(duration * 10):  # 100ms intervals
                            if not self.running:
                                break
                            time.sleep(0.1)
                            
            except Exception as e:
                self.logger.error(f"Error en ciclo del semáforo: {e}")
                time.sleep(1)
    
    def handle_emergency_override(self, command):
        """Maneja comandos de emergencia del servidor"""
        emergency_state = command.get('state', 'RED')
        try:
            new_state = TrafficLightState[emergency_state.upper()]
            self.logger.warning(f"EMERGENCIA: Cambiando a {emergency_state}")
            self.change_state(new_state)
            time.sleep(5)  # Mantener estado de emergencia
        except KeyError:
            self.logger.error(f"Estado de emergencia inválido: {emergency_state}")
    
    def communication_thread(self):
        """Hilo para manejar comunicación con el servidor"""
        while self.running:
            try:
                command = self.receive_command_from_server()
                if command:
                    self.handle_server_command(command)
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Error en hilo de comunicación: {e}")
                time.sleep(1)
    
    def handle_server_command(self, command):
        """Procesa comandos del servidor"""
        command_type = command.get('type')
        
        if command_type == 'sync_request':
            # Enviar estado actual para sincronización
            self.send_state_to_server(self.current_state, time.time())
            
        elif command_type == 'state_change':
            # Cambio de estado solicitado por el servidor
            new_state = command.get('state')
            try:
                state = TrafficLightState[new_state.upper()]
                self.change_state(state)
            except KeyError:
                self.logger.error(f"Estado inválido recibido: {new_state}")
    
    def start(self):
        """Inicia el semáforo y sus hilos"""
        if self.running:
            return
            
        self.running = True
        
        # Conectar al servidor
        if not self.connect_to_server():
            self.logger.error("No se pudo conectar al servidor")
            return False
        
        # Iniciar hilos
        cycle_thread = threading.Thread(target=self.traffic_light_cycle, daemon=True)
        comm_thread = threading.Thread(target=self.communication_thread, daemon=True)
        
        self.threads = [cycle_thread, comm_thread]
        
        for thread in self.threads:
            thread.start()
            
        self.logger.info(f"Semáforo {self.light_id} iniciado")
        return True
    
    def stop(self):
        """Detiene el semáforo y sus hilos"""
        self.running = False
        
        # Esperar a que terminen los hilos
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
        
        # Desconectar del servidor
        self.disconnect_from_server()
        
        self.logger.info(f"Semáforo {self.light_id} detenido")
    
    def get_status(self):
        """Obtiene el estado actual del semáforo de forma thread-safe"""
        with self.state_lock:
            return {
                'id': self.light_id,
                'intersection': self.intersection_name,
                'state': self.current_state.name,
                'position': (self.position_x, self.position_y),
                'state_changes': self.state_changes,
                'connected': self.connected,
                'last_sync': self.last_sync_time
            }
    
    def __str__(self):
        status = self.get_status()
        return f"Semáforo {status['id']} ({status['intersection']}): {status['state']}"
