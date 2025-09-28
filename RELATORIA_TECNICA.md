# Relatoría Técnica - SIGET
## Sistema de Gestión de Tráfico Urbano con Concurrencia

---

## 1. Introducción y Contexto

### 1.1 Descripción del Problema

El proyecto SIGET (Sistema de Gestión de Tráfico Urbano) aborda el desafío de coordinar múltiples semáforos inteligentes en una ciudad mediante un servidor central. Este escenario representa un **sistema distribuido simplificado** donde la concurrencia y la sincronización son fundamentales para mantener el orden del tráfico urbano.

### 1.2 Objetivos Académicos

El proyecto demuestra la implementación práctica de conceptos de concurrencia en sistemas operativos:

- **Comunicación Interprocesos**: Sockets TCP para coordinación distribuida
- **Sincronización**: Mutex, semáforos y locks para prevenir condiciones de carrera
- **Prevención de Deadlocks**: Algoritmos de ordenamiento de recursos
- **Gestión de Recursos**: Optimización del uso de CPU y memoria del sistema operativo

---

## 2. Lógica de Implementación

### 2.1 Arquitectura del Sistema

El sistema SIGET implementa una **arquitectura cliente-servidor distribuida** con los siguientes componentes:

```
┌─────────────────────────────────────────────────────────────┐
│                    SERVIDOR CENTRAL                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ Coordinador │ │Sincronizador│ │    Monitor del      │   │
│  │ de Tráfico  │ │ de Estados  │ │     Sistema         │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────▼───┐ ┌───▼───┐ ┌───▼───┐
            │Semáforo 1 │ │Semáforo│ │Semáforo│
            │(Centro)   │ │   2    │ │   3    │
            └───────────┘ └────────┘ └────────┘
```

### 2.2 Flujo de Comunicación

1. **Registro Inicial**: Los semáforos se conectan al servidor central
2. **Sincronización Continua**: El servidor coordina cambios de estado
3. **Monitoreo en Tiempo Real**: Supervisión del estado de cada semáforo
4. **Manejo de Emergencias**: Capacidad de override para situaciones críticas

### 2.3 Implementación de Concurrencia

#### 2.3.1 Threading y Paralelismo

```python
# Servidor central con múltiples hilos
def start_processing_threads(self):
    # Hilo para procesar mensajes
    message_thread = threading.Thread(target=self.process_messages, daemon=True)
    
    # Hilo para sincronización periódica
    sync_thread = threading.Thread(target=self.periodic_sync, daemon=True)
    
    # Hilo para monitoreo del sistema
    monitor_thread = threading.Thread(target=self.system_monitor, daemon=True)
```

#### 2.3.2 Sincronización de Recursos

```python
# Mutex para proteger estado individual
self.state_lock = threading.Lock()

# Lock reentrante para operaciones complejas
self.clients_lock = threading.RLock()

# Semáforo para control de concurrencia
self.sync_semaphore = threading.Semaphore(MAX_SEMAPHORES)
```

---

## 3. Elementos de Concurrencia Utilizados

### 3.1 Mecanismos de Sincronización

#### 3.1.1 Mutex (Mutual Exclusion)

**Implementación**: `threading.Lock()`
**Propósito**: Proteger secciones críticas del código
**Uso**: Cada semáforo tiene su propio mutex para proteger el estado

```python
def change_state(self, new_state):
    with self.state_lock:  # Mutex para proteger cambio de estado
        if self.current_state != new_state:
            self.previous_state = self.current_state
            self.current_state = new_state
```

#### 3.1.2 Semáforos

**Implementación**: `threading.Semaphore()`
**Propósito**: Controlar el número de procesos que pueden acceder a un recurso
**Uso**: Limitar el número de operaciones de sincronización simultáneas

```python
# Control de concurrencia en sincronización
with self.sync_semaphore:
    self.change_state(state)
    duration = self.get_state_duration(state)
```

#### 3.1.3 Locks Reentrantes

**Implementación**: `threading.RLock()`
**Propósito**: Permitir que el mismo hilo adquiera el lock múltiples veces
**Uso**: Operaciones complejas que requieren múltiples niveles de sincronización

```python
def process_client_message(self, client_id, message, client_socket, address):
    with self.clients_lock:  # Lock reentrante
        # Operaciones que pueden requerir el mismo lock
        self.update_client_state(client_id, message)
```

### 3.2 Comunicación Interprocesos

#### 3.2.1 Sockets TCP

**Implementación**: `socket.socket()`
**Propósito**: Comunicación bidireccional entre servidor y clientes
**Características**:
- Conexión confiable
- Transmisión de datos estructurados (JSON)
- Manejo de desconexiones

```python
def send_state_to_server(self, state, timestamp):
    message = {
        'type': 'state_update',
        'light_id': self.light_id,
        'state': state.name,
        'timestamp': timestamp
    }
    data = json.dumps(message).encode('utf-8')
    self.socket.send(data)
```

#### 3.2.2 Colas Thread-Safe

**Implementación**: `queue.Queue()`
**Propósito**: Comunicación asíncrona entre hilos
**Uso**: Buffer de mensajes para procesamiento diferido

```python
# Cola thread-safe para mensajes
self.message_queue = Queue()

def process_messages(self):
    while self.running:
        message = self.message_queue.get(timeout=1)
        self.handle_queued_message(message)
```

---

## 4. Prevención de Deadlocks

### 4.1 Algoritmo de Ordenamiento de Recursos

**Problema**: Adquisición circular de recursos puede causar deadlocks
**Solución**: Orden fijo para adquisición de recursos

```python
def acquire_locks_in_order(self, lock_names):
    """
    Implementa prevención de deadlocks por ordenamiento de recursos
    """
    # Orden predefinido de recursos
    self.resource_order = ['system_lock', 'clients_lock', 'message_lock']
    
    # Ordenar locks según el orden predefinido
    sorted_locks = sorted(lock_names, 
                         key=lambda x: self.resource_order.index(x) 
                         if x in self.resource_order else 999)
    
    for lock_name in sorted_locks:
        if lock_name == 'clients_lock':
            self.clients_lock.acquire()
```

### 4.2 Timeouts y Recuperación

**Implementación**: Timeouts en operaciones de red y sincronización
**Propósito**: Evitar bloqueos indefinidos

```python
# Timeout en comunicación
self.socket.settimeout(5)

# Timeout en sincronización
threading.Timer(5.0, self.complete_synchronization).start()
```

---

## 5. Relación con la Teoría de Sistemas Operativos

### 5.1 "¿Cómo puede un sistema operativo prevenir el colapso en la gestión de procesos?"

El proyecto SIGET demuestra múltiples estrategias para prevenir el colapso del sistema:

#### 5.1.1 Gestión de Recursos

```python
# Control de recursos limitados
MAX_CONNECTIONS = 10
MAX_SEMAPHORES = 5

# Liberación ordenada de recursos
def stop_server(self):
    self.running = False
    # Cerrar conexiones
    for client_socket in self.client_sockets.values():
        client_socket.close()
    # Liberar locks
    self.release_locks(acquired_locks)
```

#### 5.1.2 Monitoreo Continuo

```python
def system_monitor(self):
    """Monitorea el estado del sistema y detecta problemas"""
    while self.running:
        # Verificar clientes inactivos
        current_time = time.time()
        inactive_clients = []
        
        for client_id, client_info in self.clients.items():
            if current_time - client_info['last_heartbeat'] > 60:
                inactive_clients.append(client_id)
```

#### 5.1.3 Recuperación de Errores

```python
def handle_client(self, client_socket, address):
    try:
        # Procesar cliente
        while self.running:
            data = client_socket.recv(1024)
            # ... procesamiento
    except Exception as e:
        self.logger.error(f"Error manejando cliente: {e}")
    finally:
        # Limpiar recursos
        self.remove_client(client_id)
        client_socket.close()
```

### 5.2 "Mantener ocupada la CPU al 100%"

El sistema implementa estrategias para optimizar el uso de CPU:

#### 5.2.1 Procesamiento Concurrente

```python
# Múltiples hilos procesando simultáneamente
def start_processing_threads(self):
    threads = [
        threading.Thread(target=self.process_messages, daemon=True),
        threading.Thread(target=self.periodic_sync, daemon=True),
        threading.Thread(target=self.system_monitor, daemon=True)
    ]
    for thread in threads:
        thread.start()
```

#### 5.2.2 Polling Eficiente

```python
def process_messages(self):
    while self.running:
        try:
            message = self.message_queue.get(timeout=1)
            self.handle_queued_message(message)
        except Empty:
            continue  # No bloquear si no hay mensajes
```

#### 5.2.3 Carga de Trabajo Distribuida

```python
# Distribución de carga entre hilos
def accept_connections(self):
    while self.running:
        client_socket, address = self.server_socket.accept()
        # Crear hilo dedicado para cada cliente
        client_thread = threading.Thread(
            target=self.handle_client,
            args=(client_socket, address),
            daemon=True
        )
        client_thread.start()
```

---

## 6. Análisis de Problemas de Concurrencia

### 6.1 Condiciones de Carrera Identificadas

#### 6.1.1 Modificación Concurrente del Estado

**Problema**: Múltiples hilos modificando el estado del semáforo simultáneamente
**Solución**: Mutex individual por semáforo

```python
def change_state(self, new_state):
    with self.state_lock:  # Protección contra condiciones de carrera
        if self.current_state != new_state:
            self.current_state = new_state
```

#### 6.1.2 Acceso Concurrente a la Lista de Clientes

**Problema**: Múltiples hilos accediendo a la lista de clientes
**Solución**: Lock reentrante para operaciones complejas

```python
def update_client_state(self, client_id, message):
    with self.clients_lock:  # Protección de acceso concurrente
        if client_id in self.clients:
            self.clients[client_id]['state'] = message.get('state')
```

### 6.2 Deadlocks Analizados

#### 6.2.1 Adquisición Circular de Locks

**Escenario**: Hilo A adquiere lock1, luego lock2; Hilo B adquiere lock2, luego lock1
**Solución**: Ordenamiento fijo de recursos

```python
# Orden predefinido para prevenir deadlocks
self.resource_order = ['system_lock', 'clients_lock', 'message_lock']
```

#### 6.2.2 Bloqueo en Comunicación de Red

**Escenario**: Socket bloqueado esperando datos
**Solución**: Timeouts y manejo de excepciones

```python
self.socket.settimeout(1)  # Timeout para evitar bloqueo indefinido
try:
    data = self.socket.recv(1024)
except socket.timeout:
    pass  # Continuar sin bloquear
```

---

## 7. Contribución a la Fiabilidad del SIGET

### 7.1 Robustez del Sistema

El sistema implementa múltiples capas de protección:

1. **Validación de Datos**: Verificación de mensajes recibidos
2. **Manejo de Excepciones**: Recuperación automática de errores
3. **Timeouts**: Prevención de bloqueos indefinidos
4. **Logging Detallado**: Trazabilidad completa de operaciones

### 7.2 Escalabilidad

```python
# Sistema escalable con límites configurables
MAX_CONNECTIONS = 10
MAX_SEMAPHORES = 5

# Pool de hilos para manejo eficiente de clientes
def accept_connections(self):
    while self.running:
        client_socket, address = self.server_socket.accept()
        # Crear hilo dedicado para cada cliente
        client_thread = threading.Thread(target=self.handle_client, daemon=True)
        client_thread.start()
```

### 7.3 Monitoreo y Diagnóstico

```python
def log_system_stats(self):
    status = self.get_system_status()
    self.logger.info(f"Sistema SIGET - Clientes: {status['total_clients']}, "
                    f"Mensajes procesados: {status['stats']['messages_processed']}")
```

---

## 8. Reflexión Crítica

### 8.1 Ventajas de la Concurrencia Aplicada

1. **Eficiencia**: Múltiples operaciones simultáneas
2. **Responsividad**: Interfaz gráfica no se bloquea
3. **Escalabilidad**: Fácil agregar más semáforos
4. **Robustez**: Fallo de un componente no afecta el sistema completo

### 8.2 Limitaciones Identificadas

1. **Complejidad**: Mayor dificultad de debugging
2. **Overhead**: Costo de sincronización
3. **Recursos**: Mayor uso de memoria y CPU
4. **Debugging**: Dificultad para reproducir problemas

### 8.3 Optimización de Recursos del SO

El proyecto demuestra cómo la concurrencia puede optimizar el uso de recursos:

- **CPU**: Múltiples hilos aprovechan múltiples cores
- **Memoria**: Compartimiento eficiente de datos
- **Red**: Comunicación asíncrona no bloqueante
- **I/O**: Operaciones de red en paralelo

---

## 9. Conclusiones

El proyecto SIGET demuestra exitosamente la implementación práctica de conceptos de concurrencia en sistemas operativos. La solución propuesta:

1. **Resuelve el problema real** de coordinación de semáforos urbanos
2. **Implementa mecanismos robustos** de sincronización y comunicación
3. **Previene problemas clásicos** de concurrencia como deadlocks y condiciones de carrera
4. **Optimiza el uso de recursos** del sistema operativo
5. **Proporciona una interfaz visual** para demostrar el comportamiento concurrente

La implementación conecta directamente con la teoría de sistemas operativos, mostrando cómo los conceptos académicos se aplican en sistemas reales para mejorar la eficiencia y confiabilidad de la gestión de recursos computacionales.

---

**Fecha**: 2024  
**Autor**: [Tu Nombre]  
**Curso**: Concurrencia en Sistemas Operativos  
**Universidad**: [Nombre de la Universidad]
