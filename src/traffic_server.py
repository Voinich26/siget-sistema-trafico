"""
Servidor Central SIGET
Maneja la coordinación y sincronización de múltiples semáforos
Implementa concurrencia y prevención de deadlocks
"""

import socket
import threading
import time
import json
import logging
from collections import defaultdict, deque
from queue import Queue, Empty
from src.config import *

class TrafficServer:
    """
    Servidor central que coordina múltiples semáforos
    Implementa mecanismos de concurrencia y sincronización
    """
    
    def __init__(self):
        # Configuración del servidor
        self.host = SERVER_HOST
        self.port = SERVER_PORT
        self.running = False
        
        # Sincronización
        self.clients_lock = threading.RLock()  # Lock reentrante para evitar deadlocks
        self.message_queue = Queue()  # Cola thread-safe para mensajes
        self.sync_semaphore = threading.Semaphore(MAX_SEMAPHORES)  # Control de concurrencia
        
        # Almacenamiento de clientes (semáforos)
        self.clients = {}  # {client_id: client_info}
        self.client_sockets = {}  # {client_id: socket}
        self.client_locks = {}  # {client_id: lock} - Lock individual por cliente
        
        # Estado del sistema
        self.system_state = {
            'emergency_mode': False,
            'sync_in_progress': False,
            'last_sync': time.time(),
            'total_clients': 0
        }
        
        # Prevención de deadlocks - orden fijo para adquisición de recursos
        self.resource_order = ['system_lock', 'clients_lock', 'message_lock']
        self.active_locks = set()
        
        # Logging
        self.logger = logging.getLogger('TrafficServer')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Estadísticas
        self.stats = {
            'messages_processed': 0,
            'sync_operations': 0,
            'emergency_overrides': 0,
            'deadlock_preventions': 0
        }
        
        # Hilos del servidor
        self.threads = []
        
    def acquire_locks_in_order(self, lock_names):
        """
        Adquiere locks en orden fijo para prevenir deadlocks
        Implementa el algoritmo de prevención de deadlocks por ordenamiento
        """
        acquired_locks = []
        
        try:
            # Ordenar locks según el orden predefinido
            sorted_locks = sorted(lock_names, key=lambda x: self.resource_order.index(x) if x in self.resource_order else 999)
            
            for lock_name in sorted_locks:
                if lock_name == 'system_lock':
                    # Lock del sistema (simulado)
                    pass
                elif lock_name == 'clients_lock':
                    self.clients_lock.acquire()
                    acquired_locks.append('clients_lock')
                elif lock_name == 'message_lock':
                    # Lock de mensajes (simulado)
                    pass
                    
            self.active_locks.update(acquired_locks)
            self.stats['deadlock_preventions'] += 1
            return acquired_locks
            
        except Exception as e:
            # Liberar locks adquiridos en caso de error
            self.release_locks(acquired_locks)
            raise e
    
    def release_locks(self, lock_names):
        """Libera locks en orden inverso"""
        for lock_name in reversed(lock_names):
            if lock_name == 'clients_lock':
                try:
                    self.clients_lock.release()
                except RuntimeError:
                    # El lock ya estaba liberado
                    pass
            self.active_locks.discard(lock_name)
    
    def start_server(self):
        """Inicia el servidor y sus hilos de procesamiento"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAX_CONNECTIONS)
            
            self.running = True
            self.logger.info(f"Servidor SIGET iniciado en {self.host}:{self.port}")
            
            # Iniciar hilos de procesamiento
            self.start_processing_threads()
            
            # Hilo principal para aceptar conexiones
            accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
            accept_thread.start()
            self.threads.append(accept_thread)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error iniciando servidor: {e}")
            return False
    
    def start_processing_threads(self):
        """Inicia hilos de procesamiento concurrente"""
        # Hilo para procesar mensajes
        message_thread = threading.Thread(target=self.process_messages, daemon=True)
        message_thread.start()
        self.threads.append(message_thread)
        
        # Hilo para sincronización periódica
        sync_thread = threading.Thread(target=self.periodic_sync, daemon=True)
        sync_thread.start()
        self.threads.append(sync_thread)
        
        # Hilo para monitoreo del sistema
        monitor_thread = threading.Thread(target=self.system_monitor, daemon=True)
        monitor_thread.start()
        self.threads.append(monitor_thread)
    
    def accept_connections(self):
        """Acepta conexiones de semáforos de forma concurrente"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.logger.info(f"Nueva conexión desde {address}")
                
                # Crear hilo para manejar cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                self.threads.append(client_thread)
                
            except Exception as e:
                if self.running:
                    self.logger.error(f"Error aceptando conexión: {e}")
                break
    
    def handle_client(self, client_socket, address):
        """Maneja la comunicación con un cliente específico"""
        client_id = None
        
        try:
            while self.running:
                # Recibir mensaje del cliente
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = json.loads(data.decode('utf-8'))
                client_id = message.get('light_id')
                
                # Procesar mensaje de forma thread-safe
                self.process_client_message(client_id, message, client_socket, address)
                
        except Exception as e:
            self.logger.error(f"Error manejando cliente {address}: {e}")
        finally:
            # Limpiar recursos del cliente
            if client_id:
                self.remove_client(client_id)
            client_socket.close()
            self.logger.info(f"Cliente {address} desconectado")
    
    def process_client_message(self, client_id, message, client_socket, address):
        """Procesa mensaje de cliente de forma thread-safe"""
        message_type = message.get('type')
        
        # Adquirir locks necesarios
        locks_to_acquire = ['clients_lock']
        if message_type == 'state_update':
            locks_to_acquire.append('system_lock')
        
        acquired_locks = self.acquire_locks_in_order(locks_to_acquire)
        
        try:
            if message_type == 'register':
                self.register_client(client_id, message, client_socket, address)
            elif message_type == 'state_update':
                self.update_client_state(client_id, message)
            elif message_type == 'heartbeat':
                self.update_client_heartbeat(client_id)
            else:
                self.logger.warning(f"Tipo de mensaje desconocido: {message_type}")
                
            self.stats['messages_processed'] += 1
            
        finally:
            self.release_locks(acquired_locks)
    
    def register_client(self, client_id, message, client_socket, address):
        """Registra un nuevo semáforo en el sistema"""
        client_info = {
            'id': client_id,
            'intersection': message.get('intersection', 'Unknown'),
            'position': message.get('position', (0, 0)),
            'state': message.get('state', 'RED'),
            'last_heartbeat': time.time(),
            'socket': client_socket,
            'address': address,
            'state_changes': 0
        }
        
        self.clients[client_id] = client_info
        self.client_sockets[client_id] = client_socket
        self.client_locks[client_id] = threading.Lock()
        self.system_state['total_clients'] = len(self.clients)
        
        self.logger.info(f"Cliente {client_id} registrado: {client_info['intersection']}")
        
        # Enviar confirmación de registro
        self.send_to_client(client_id, {
            'type': 'registration_confirmed',
            'server_time': time.time(),
            'client_id': client_id
        })
    
    def update_client_state(self, client_id, message):
        """Actualiza el estado de un semáforo"""
        if client_id not in self.clients:
            return
            
        client_info = self.clients[client_id]
        client_info['state'] = message.get('state', client_info['state'])
        client_info['last_heartbeat'] = time.time()
        client_info['state_changes'] += 1
        
        self.logger.debug(f"Estado actualizado para {client_id}: {client_info['state']}")
        
        # Verificar si se necesita sincronización
        if self.should_sync_clients():
            self.trigger_synchronization()
    
    def update_client_heartbeat(self, client_id):
        """Actualiza el heartbeat de un cliente"""
        if client_id in self.clients:
            self.clients[client_id]['last_heartbeat'] = time.time()
    
    def should_sync_clients(self):
        """Determina si se necesita sincronización entre semáforos"""
        if self.system_state['sync_in_progress']:
            return False
            
        # Sincronizar si han pasado más de 30 segundos desde la última sincronización
        return (time.time() - self.system_state['last_sync']) > 30
    
    def trigger_synchronization(self):
        """Inicia proceso de sincronización entre semáforos"""
        if self.system_state['sync_in_progress']:
            return
            
        self.system_state['sync_in_progress'] = True
        self.system_state['last_sync'] = time.time()
        self.stats['sync_operations'] += 1
        
        self.logger.info("Iniciando sincronización de semáforos")
        
        # Enviar comando de sincronización a todos los clientes
        sync_message = {
            'type': 'sync_request',
            'timestamp': time.time(),
            'server_id': 'SIGET_CENTRAL'
        }
        
        self.broadcast_message(sync_message)
        
        # Marcar sincronización como completada después de un tiempo
        threading.Timer(5.0, self.complete_synchronization).start()
    
    def complete_synchronization(self):
        """Marca la sincronización como completada"""
        self.system_state['sync_in_progress'] = False
        self.logger.info("Sincronización completada")
    
    def process_messages(self):
        """Procesa mensajes de la cola de forma concurrente"""
        while self.running:
            try:
                # Procesar mensajes de la cola
                message = self.message_queue.get(timeout=1)
                self.handle_queued_message(message)
                self.message_queue.task_done()
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error procesando mensaje: {e}")
    
    def handle_queued_message(self, message):
        """Maneja mensajes de la cola"""
        # Implementar lógica específica para mensajes en cola
        pass
    
    def periodic_sync(self):
        """Realiza sincronización periódica del sistema"""
        while self.running:
            try:
                time.sleep(30)  # Sincronizar cada 30 segundos
                
                if self.should_sync_clients():
                    self.trigger_synchronization()
                    
            except Exception as e:
                self.logger.error(f"Error en sincronización periódica: {e}")
    
    def system_monitor(self):
        """Monitorea el estado del sistema y detecta problemas"""
        while self.running:
            try:
                time.sleep(10)  # Monitorear cada 10 segundos
                
                # Verificar clientes inactivos
                current_time = time.time()
                inactive_clients = []
                
                with self.clients_lock:
                    for client_id, client_info in self.clients.items():
                        if current_time - client_info['last_heartbeat'] > 60:  # 60 segundos sin heartbeat
                            inactive_clients.append(client_id)
                
                # Remover clientes inactivos
                for client_id in inactive_clients:
                    self.remove_client(client_id)
                    self.logger.warning(f"Cliente {client_id} marcado como inactivo")
                
                # Log estadísticas del sistema
                self.log_system_stats()
                
            except Exception as e:
                self.logger.error(f"Error en monitoreo del sistema: {e}")
    
    def remove_client(self, client_id):
        """Remueve un cliente del sistema de forma thread-safe"""
        with self.clients_lock:
            if client_id in self.clients:
                del self.clients[client_id]
                if client_id in self.client_sockets:
                    del self.client_sockets[client_id]
                if client_id in self.client_locks:
                    del self.client_locks[client_id]
                self.system_state['total_clients'] = len(self.clients)
                self.logger.info(f"Cliente {client_id} removido del sistema")
    
    def send_to_client(self, client_id, message):
        """Envía mensaje a un cliente específico"""
        if client_id not in self.client_sockets:
            return False
            
        try:
            client_socket = self.client_sockets[client_id]
            data = json.dumps(message).encode('utf-8')
            client_socket.send(data)
            return True
        except Exception as e:
            self.logger.error(f"Error enviando mensaje a {client_id}: {e}")
            return False
    
    def broadcast_message(self, message):
        """Envía mensaje a todos los clientes conectados"""
        with self.clients_lock:
            for client_id in list(self.client_sockets.keys()):
                self.send_to_client(client_id, message)
    
    def emergency_override(self, target_intersection=None, emergency_state='RED'):
        """Activa modo de emergencia para semáforos específicos o todos"""
        self.system_state['emergency_mode'] = True
        self.stats['emergency_overrides'] += 1
        
        self.logger.warning(f"ACTIVANDO MODO DE EMERGENCIA: {emergency_state}")
        
        message = {
            'type': 'emergency_override',
            'state': emergency_state,
            'timestamp': time.time(),
            'target_intersection': target_intersection
        }
        
        if target_intersection:
            # Enviar solo a semáforos de la intersección específica
            with self.clients_lock:
                for client_id, client_info in self.clients.items():
                    if client_info['intersection'] == target_intersection:
                        self.send_to_client(client_id, message)
        else:
            # Enviar a todos los semáforos
            self.broadcast_message(message)
    
    def get_system_status(self):
        """Obtiene el estado actual del sistema"""
        with self.clients_lock:
            return {
                'running': self.running,
                'total_clients': len(self.clients),
                'clients': {cid: {
                    'intersection': info['intersection'],
                    'state': info['state'],
                    'last_heartbeat': info['last_heartbeat'],
                    'state_changes': info['state_changes']
                } for cid, info in self.clients.items()},
                'system_state': self.system_state.copy(),
                'stats': self.stats.copy(),
                'active_locks': list(self.active_locks)
            }
    
    def log_system_stats(self):
        """Registra estadísticas del sistema"""
        status = self.get_system_status()
        self.logger.info(f"Sistema SIGET - Clientes: {status['total_clients']}, "
                        f"Mensajes procesados: {status['stats']['messages_processed']}, "
                        f"Sincronizaciones: {status['stats']['sync_operations']}")
    
    def stop_server(self):
        """Detiene el servidor y libera recursos"""
        self.running = False
        
        # Cerrar conexiones con clientes
        with self.clients_lock:
            for client_socket in self.client_sockets.values():
                try:
                    client_socket.close()
                except:
                    pass
        
        # Cerrar socket del servidor
        try:
            self.server_socket.close()
        except:
            pass
        
        # Esperar a que terminen los hilos
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
        
        self.logger.info("Servidor SIGET detenido")
    
    def __str__(self):
        status = self.get_system_status()
        return f"Servidor SIGET - {status['total_clients']} clientes conectados"
