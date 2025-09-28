"""
Tests unitarios para el sistema SIGET
Pruebas de concurrencia y sincronización
"""

import unittest
import threading
import time
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.traffic_light import TrafficLight, TrafficLightState
from src.config import *

class TestTrafficLight(unittest.TestCase):
    """Tests para la clase TrafficLight"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.traffic_light = TrafficLight("TEST001", "Intersección de Prueba", 0, 0)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if hasattr(self, 'traffic_light'):
            self.traffic_light.stop()
    
    def test_initial_state(self):
        """Test del estado inicial del semáforo"""
        self.assertEqual(self.traffic_light.current_state, TrafficLightState.RED)
        self.assertEqual(self.traffic_light.light_id, "TEST001")
        self.assertEqual(self.traffic_light.intersection_name, "Intersección de Prueba")
    
    def test_state_change_thread_safety(self):
        """Test de thread-safety en cambios de estado"""
        def change_state_multiple_times():
            for _ in range(100):
                self.traffic_light.change_state(TrafficLightState.GREEN)
                time.sleep(0.001)
                self.traffic_light.change_state(TrafficLightState.RED)
                time.sleep(0.001)
        
        # Crear múltiples hilos que cambien el estado
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=change_state_multiple_times)
            threads.append(thread)
            thread.start()
        
        # Esperar a que terminen todos los hilos
        for thread in threads:
            thread.join()
        
        # Verificar que no hubo condiciones de carrera
        self.assertIsInstance(self.traffic_light.current_state, TrafficLightState)
        self.assertGreater(self.traffic_light.state_changes, 0)
    
    def test_state_duration(self):
        """Test de duración de estados"""
        red_duration = self.traffic_light.get_state_duration(TrafficLightState.RED)
        green_duration = self.traffic_light.get_state_duration(TrafficLightState.GREEN)
        yellow_duration = self.traffic_light.get_state_duration(TrafficLightState.YELLOW)
        
        self.assertEqual(red_duration, STATE_DURATIONS['RED'])
        self.assertEqual(green_duration, STATE_DURATIONS['GREEN'])
        self.assertEqual(yellow_duration, STATE_DURATIONS['YELLOW'])
    
    def test_status_thread_safety(self):
        """Test de thread-safety en obtención de estado"""
        def get_status_multiple_times():
            for _ in range(50):
                status = self.traffic_light.get_status()
                self.assertIn('id', status)
                self.assertIn('state', status)
                time.sleep(0.001)
        
        # Crear múltiples hilos que obtengan el estado
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=get_status_multiple_times)
            threads.append(thread)
            thread.start()
        
        # Esperar a que terminen todos los hilos
        for thread in threads:
            thread.join()

class TestConcurrency(unittest.TestCase):
    """Tests específicos de concurrencia"""
    
    def test_deadlock_prevention(self):
        """Test de prevención de deadlocks"""
        from src.traffic_server import TrafficServer
        
        server = TrafficServer()
        
        # Simular adquisición de locks en orden
        lock_names = ['clients_lock', 'system_lock']
        acquired_locks = server.acquire_locks_in_order(lock_names)
        
        # Verificar que se adquirieron en orden
        self.assertIn('clients_lock', acquired_locks)
        
        # Liberar locks
        server.release_locks(acquired_locks)
    
    def test_semaphore_control(self):
        """Test de control de semáforos"""
        from src.traffic_server import TrafficServer
        
        server = TrafficServer()
        
        # Verificar que el semáforo inicial está disponible
        self.assertTrue(server.sync_semaphore.acquire(blocking=False))
        server.sync_semaphore.release()
    
    def test_message_queue_thread_safety(self):
        """Test de thread-safety en cola de mensajes"""
        from queue import Queue
        import threading
        
        message_queue = Queue()
        results = []
        
        def producer():
            for i in range(100):
                message_queue.put(f"message_{i}")
                time.sleep(0.001)
        
        def consumer():
            while True:
                try:
                    message = message_queue.get(timeout=1)
                    results.append(message)
                    message_queue.task_done()
                except:
                    break
        
        # Crear hilos productor y consumidor
        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)
        
        producer_thread.start()
        consumer_thread.start()
        
        producer_thread.join()
        message_queue.join()  # Esperar a que se procesen todos los mensajes
        
        # Verificar que se procesaron todos los mensajes
        self.assertEqual(len(results), 100)

class TestSystemIntegration(unittest.TestCase):
    """Tests de integración del sistema"""
    
    def test_config_loading(self):
        """Test de carga de configuración"""
        from src.config import COLORS, STATE_DURATIONS, SERVER_PORT
        
        self.assertIsInstance(COLORS, dict)
        self.assertIn('background', COLORS)
        self.assertIn('primary', COLORS)
        
        self.assertIsInstance(STATE_DURATIONS, dict)
        self.assertIn('RED', STATE_DURATIONS)
        self.assertIn('GREEN', STATE_DURATIONS)
        self.assertIn('YELLOW', STATE_DURATIONS)
        
        self.assertIsInstance(SERVER_PORT, int)
        self.assertGreater(SERVER_PORT, 0)

if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.WARNING)  # Reducir verbosidad en tests
    
    # Ejecutar tests
    unittest.main(verbosity=2)
