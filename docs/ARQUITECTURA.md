# Arquitectura del Sistema SIGET

## Visión General

SIGET implementa una **arquitectura distribuida cliente-servidor** que simula un sistema de gestión de tráfico urbano. El sistema está diseñado para demostrar conceptos de concurrencia, sincronización y comunicación interprocesos en sistemas operativos.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    SERVIDOR CENTRAL SIGET                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Coordinador   │  │  Sincronizador  │  │    Monitor      │ │
│  │   de Tráfico    │  │   de Estados    │  │   del Sistema   │ │
│  │                 │  │                 │  │                 │ │
│  │ • Gestión de    │  │ • Coordinación  │  │ • Health Check  │ │
│  │   clientes      │  │   temporal      │  │ • Estadísticas  │ │
│  │ • Comunicación  │  │ • Prevención    │  │ • Logging       │ │
│  │   TCP/IP        │  │   deadlocks     │  │ • Recuperación  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────▼───┐ ┌───▼───┐ ┌───▼───┐
            │Semáforo 1 │ │Semáforo│ │Semáforo│
            │(Centro)   │ │   2    │ │   3    │
            │           │ │(Norte) │ │(Sur)   │
            │ • Estados │ │        │ │        │
            │ • Ciclos  │ │ • Estados│ │ • Estados│
            │ • Sync    │ │ • Ciclos │ │ • Ciclos │
            │ • Comm    │ │ • Sync   │ │ • Sync   │
            └───────────┘ └────────┘ └────────┘
```

## Componentes del Sistema

### 1. Servidor Central (`TrafficServer`)

**Responsabilidades:**
- Coordinación de múltiples semáforos
- Sincronización de estados
- Monitoreo del sistema
- Manejo de emergencias
- Comunicación TCP/IP

**Características Técnicas:**
- **Threading**: Múltiples hilos para procesamiento concurrente
- **Sockets TCP**: Comunicación confiable con clientes
- **Sincronización**: Locks y semáforos para thread-safety
- **Prevención de Deadlocks**: Algoritmos de ordenamiento de recursos

```python
class TrafficServer:
    def __init__(self):
        self.clients_lock = threading.RLock()  # Lock reentrante
        self.sync_semaphore = threading.Semaphore(MAX_SEMAPHORES)
        self.message_queue = Queue()  # Cola thread-safe
```

### 2. Semáforos Inteligentes (`TrafficLight`)

**Responsabilidades:**
- Ciclos de estados (ROJO → VERDE → AMARILLO)
- Comunicación con servidor central
- Sincronización de estados
- Manejo de emergencias

**Estados del Semáforo:**
```python
class TrafficLightState(Enum):
    RED = 0      # Detener tráfico
    YELLOW = 1   # Precaución
    GREEN = 2    # Avanzar
```

**Características Técnicas:**
- **Threading**: Hilos separados para ciclo y comunicación
- **Mutex**: Protección del estado individual
- **Heartbeat**: Monitoreo de conectividad
- **Recovery**: Recuperación automática de errores

### 3. Interfaz Gráfica (`SIGETGUI`)

**Responsabilidades:**
- Visualización en tiempo real
- Control del sistema
- Monitoreo de logs
- Estadísticas del sistema

**Características Técnicas:**
- **Tkinter**: Interfaz gráfica nativa
- **Threading**: Actualización asíncrona de la UI
- **Animaciones**: Transiciones suaves entre estados
- **Logging**: Visualización de logs en tiempo real

## Flujo de Comunicación

### 1. Inicialización del Sistema

```
Cliente (Semáforo)          Servidor Central
     │                           │
     ├─── connect() ────────────►│
     │                           │
     ├─── register() ───────────►│
     │                           │
     │◄── registration_confirmed─┤
     │                           │
     ├─── start_cycle() ────────►│
     │                           │
```

### 2. Ciclo Normal de Operación

```
Semáforo                     Servidor
     │                           │
     ├─── state_update ────────►│
     │                           │
     │◄── sync_request ──────────┤
     │                           │
     ├─── current_state ───────►│
     │                           │
     │◄── sync_complete ─────────┤
     │                           │
```

### 3. Manejo de Emergencias

```
Usuario                      Servidor                     Semáforos
     │                           │                           │
     ├─── emergency_override ───►│                           │
     │                           │                           │
     │                           ├─── emergency_override ───►│
     │                           │                           │
     │                           │◄── emergency_ack ─────────┤
     │                           │                           │
```

## Mecanismos de Concurrencia

### 1. Threading y Paralelismo

**Servidor Central:**
- **Hilo Principal**: Acepta conexiones de clientes
- **Hilo de Mensajes**: Procesa mensajes de la cola
- **Hilo de Sincronización**: Coordina estados periódicamente
- **Hilo de Monitoreo**: Supervisa el estado del sistema

**Semáforos:**
- **Hilo de Ciclo**: Ejecuta el ciclo de estados
- **Hilo de Comunicación**: Maneja comunicación con servidor

### 2. Sincronización

**Mutex (Mutual Exclusion):**
```python
self.state_lock = threading.Lock()  # Protege estado individual
```

**Locks Reentrantes:**
```python
self.clients_lock = threading.RLock()  # Permite adquisición anidada
```

**Semáforos:**
```python
self.sync_semaphore = threading.Semaphore(MAX_SEMAPHORES)  # Control de concurrencia
```

**Colas Thread-Safe:**
```python
self.message_queue = Queue()  # Comunicación asíncrona
```

### 3. Prevención de Deadlocks

**Algoritmo de Ordenamiento de Recursos:**
```python
def acquire_locks_in_order(self, lock_names):
    # Orden predefinido para prevenir deadlocks
    self.resource_order = ['system_lock', 'clients_lock', 'message_lock']
    sorted_locks = sorted(lock_names, key=lambda x: self.resource_order.index(x))
```

**Timeouts:**
```python
self.socket.settimeout(5)  # Evitar bloqueos indefinidos
```

## Gestión de Recursos

### 1. Memoria

**Estrategias:**
- **Pool de Conexiones**: Reutilización de sockets
- **Garbage Collection**: Liberación automática de objetos
- **Caching**: Almacenamiento de estados frecuentemente accedidos

### 2. CPU

**Optimizaciones:**
- **Threading**: Aprovechamiento de múltiples cores
- **Polling Eficiente**: Timeouts para evitar bloqueos
- **Batching**: Procesamiento por lotes de operaciones

### 3. Red

**Características:**
- **TCP**: Comunicación confiable
- **JSON**: Formato ligero para mensajes
- **Heartbeat**: Monitoreo de conectividad
- **Reconnection**: Reconexión automática

## Patrones de Diseño

### 1. Observer Pattern

Los semáforos notifican cambios de estado al servidor central.

### 2. Producer-Consumer

La cola de mensajes implementa este patrón para comunicación asíncrona.

### 3. Singleton

El servidor central es una instancia única que coordina todo el sistema.

### 4. State Machine

Los semáforos implementan una máquina de estados para sus ciclos.

## Escalabilidad

### 1. Horizontal

- **Múltiples Servidores**: Balanceador de carga
- **Distribución Geográfica**: Servidores por región
- **Microservicios**: Separación de responsabilidades

### 2. Vertical

- **Más Cores**: Aprovechamiento de threading
- **Más Memoria**: Caching y buffering
- **Mejor Red**: Redes de alta velocidad

## Seguridad

### 1. Autenticación

- **Tokens**: Identificación de semáforos
- **Heartbeat**: Verificación de conectividad
- **Timeouts**: Detección de clientes inactivos

### 2. Validación

- **Sanitización**: Validación de mensajes
- **Rate Limiting**: Control de frecuencia
- **Error Handling**: Manejo robusto de errores

## Monitoreo y Logging

### 1. Métricas del Sistema

- **Clientes Conectados**: Número de semáforos activos
- **Mensajes Procesados**: Throughput de comunicación
- **Tiempo de Respuesta**: Latencia del sistema
- **Uso de Recursos**: CPU y memoria

### 2. Logging Detallado

- **Operaciones Concurrentes**: Qué hilo ejecuta qué operación
- **Cambios de Estado**: Transiciones de estados
- **Comunicación**: Mensajes enviados/recibidos
- **Errores**: Trazabilidad completa de problemas

## Extensibilidad

### 1. Nuevos Tipos de Dispositivos

- **Sensores de Tráfico**: Detección de vehículos
- **Cámaras**: Análisis de imágenes
- **Dispositivos IoT**: Integración con sensores

### 2. Nuevas Funcionalidades

- **Machine Learning**: Predicción de patrones
- **Analytics**: Análisis de datos históricos
- **Mobile App**: Aplicación móvil para monitoreo

## Consideraciones de Rendimiento

### 1. Optimizaciones Implementadas

- **Threading**: Paralelismo real
- **Caching**: Reducción de accesos a disco
- **Batching**: Procesamiento eficiente
- **Connection Pooling**: Reutilización de conexiones

### 2. Puntos de Mejora

- **Async/Await**: Programación asíncrona
- **Redis**: Cache distribuido
- **Message Queues**: Colas de mensajes externas
- **Load Balancing**: Distribución de carga

Esta arquitectura demuestra cómo los conceptos de concurrencia y sistemas operativos se aplican en sistemas reales, proporcionando una base sólida para el aprendizaje y la experimentación con sistemas distribuidos.
