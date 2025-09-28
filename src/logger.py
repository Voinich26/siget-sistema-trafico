"""
Sistema de Logging Avanzado para SIGET
Implementa logging detallado para mostrar comportamiento concurrente
"""

import logging
import threading
import time
import json
from datetime import datetime
from pathlib import Path
from src.config import *

class ConcurrentLogger:
    """
    Logger especializado para sistemas concurrentes
    Implementa logging thread-safe con información detallada de concurrencia
    """
    
    def __init__(self, name, log_file=None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Lock para logging thread-safe
        self.log_lock = threading.Lock()
        
        # Archivo de log específico
        if log_file:
            self.log_file = Path('logs') / log_file
            self.log_file.parent.mkdir(exist_ok=True)
        else:
            self.log_file = Path('logs') / f'{name.lower()}.log'
            self.log_file.parent.mkdir(exist_ok=True)
        
        # Configurar handlers
        self.setup_handlers()
        
        # Estadísticas de logging
        self.stats = {
            'total_logs': 0,
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0,
            'debug_count': 0
        }
    
    def setup_handlers(self):
        """Configura los handlers de logging"""
        # Handler para archivo
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato personalizado
        formatter = logging.Formatter(
            '%(asctime)s | %(threadName)-10s | %(name)-20s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregar handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_concurrent_operation(self, operation, thread_id=None, **kwargs):
        """Log específico para operaciones concurrentes"""
        with self.log_lock:
            thread_name = thread_id or threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'operation': operation,
                'logger': self.name,
                **kwargs
            }
            
            message = f"OP[{operation}] | Thread[{thread_name}] | {json.dumps(kwargs, default=str)}"
            self.logger.info(message)
            self.stats['info_count'] += 1
            self.stats['total_logs'] += 1
    
    def log_state_change(self, old_state, new_state, entity_id, **kwargs):
        """Log específico para cambios de estado"""
        with self.log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'entity_id': entity_id,
                'old_state': old_state,
                'new_state': new_state,
                'logger': self.name,
                **kwargs
            }
            
            message = f"STATE_CHANGE | {entity_id} | {old_state} -> {new_state} | Thread[{thread_name}]"
            self.logger.info(message)
            self.stats['info_count'] += 1
            self.stats['total_logs'] += 1
    
    def log_synchronization(self, sync_type, resources, **kwargs):
        """Log específico para operaciones de sincronización"""
        with self.log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'sync_type': sync_type,
                'resources': resources,
                'logger': self.name,
                **kwargs
            }
            
            message = f"SYNC[{sync_type}] | Resources: {resources} | Thread[{thread_name}]"
            self.logger.info(message)
            self.stats['info_count'] += 1
            self.stats['total_logs'] += 1
    
    def log_communication(self, direction, target, message_type, **kwargs):
        """Log específico para comunicación entre procesos"""
        with self.log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'direction': direction,  # 'send' o 'receive'
                'target': target,
                'message_type': message_type,
                'logger': self.name,
                **kwargs
            }
            
            message = f"COMM[{direction.upper()}] | To: {target} | Type: {message_type} | Thread[{thread_name}]"
            self.logger.info(message)
            self.stats['info_count'] += 1
            self.stats['total_logs'] += 1
    
    def log_error(self, error_type, error_message, **kwargs):
        """Log específico para errores"""
        with self.log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'error_type': error_type,
                'error_message': error_message,
                'logger': self.name,
                **kwargs
            }
            
            message = f"ERROR[{error_type}] | {error_message} | Thread[{thread_name}]"
            self.logger.error(message)
            self.stats['error_count'] += 1
            self.stats['total_logs'] += 1
    
    def log_deadlock_prevention(self, resources, prevention_method, **kwargs):
        """Log específico para prevención de deadlocks"""
        with self.log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'resources': resources,
                'prevention_method': prevention_method,
                'logger': self.name,
                **kwargs
            }
            
            message = f"DEADLOCK_PREVENTION | Method: {prevention_method} | Resources: {resources} | Thread[{thread_name}]"
            self.logger.warning(message)
            self.stats['warning_count'] += 1
            self.stats['total_logs'] += 1
    
    def log_performance(self, operation, duration, **kwargs):
        """Log específico para métricas de rendimiento"""
        with self.log_lock:
            thread_name = threading.current_thread().name
            timestamp = time.time()
            
            log_data = {
                'timestamp': timestamp,
                'thread': thread_name,
                'operation': operation,
                'duration': duration,
                'logger': self.name,
                **kwargs
            }
            
            message = f"PERF[{operation}] | Duration: {duration:.3f}s | Thread[{thread_name}]"
            self.logger.debug(message)
            self.stats['debug_count'] += 1
            self.stats['total_logs'] += 1
    
    def get_stats(self):
        """Obtiene estadísticas del logger"""
        with self.log_lock:
            return self.stats.copy()
    
    def reset_stats(self):
        """Reinicia las estadísticas del logger"""
        with self.log_lock:
            self.stats = {
                'total_logs': 0,
                'error_count': 0,
                'warning_count': 0,
                'info_count': 0,
                'debug_count': 0
            }

class SystemLogger:
    """
    Logger central del sistema SIGET
    Coordina el logging de todos los componentes
    """
    
    def __init__(self):
        self.loggers = {}
        self.system_start_time = time.time()
        
        # Crear directorio de logs
        Path('logs').mkdir(exist_ok=True)
        
        # Logger principal del sistema
        self.main_logger = ConcurrentLogger('SIGET_MAIN', 'system.log')
        
        # Loggers específicos
        self.server_logger = ConcurrentLogger('SIGET_SERVER', 'server.log')
        self.traffic_light_logger = ConcurrentLogger('SIGET_TRAFFIC_LIGHT', 'traffic_lights.log')
        self.gui_logger = ConcurrentLogger('SIGET_GUI', 'gui.log')
        
        self.loggers = {
            'main': self.main_logger,
            'server': self.server_logger,
            'traffic_light': self.traffic_light_logger,
            'gui': self.gui_logger
        }
    
    def get_logger(self, component):
        """Obtiene el logger para un componente específico"""
        return self.loggers.get(component, self.main_logger)
    
    def log_system_start(self):
        """Log del inicio del sistema"""
        self.main_logger.log_concurrent_operation(
            'SYSTEM_START',
            system_time=self.system_start_time,
            components=list(self.loggers.keys())
        )
    
    def log_system_stop(self):
        """Log del fin del sistema"""
        uptime = time.time() - self.system_start_time
        self.main_logger.log_concurrent_operation(
            'SYSTEM_STOP',
            uptime=uptime,
            total_logs=sum(logger.get_stats()['total_logs'] for logger in self.loggers.values())
        )
    
    def get_system_stats(self):
        """Obtiene estadísticas de todo el sistema"""
        stats = {
            'system_uptime': time.time() - self.system_start_time,
            'components': {}
        }
        
        for name, logger in self.loggers.items():
            stats['components'][name] = logger.get_stats()
        
        return stats

# Instancia global del logger del sistema
system_logger = SystemLogger()

def get_logger(component='main'):
    """Función de conveniencia para obtener un logger"""
    return system_logger.get_logger(component)
