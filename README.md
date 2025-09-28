# SIGET - Sistema de Gestión de Tráfico Urbano

## Descripción del Proyecto

SIGET es un sistema distribuido de gestión de tráfico urbano desarrollado como proyecto académico para el curso de **Concurrencia en Sistemas Operativos**. El sistema simula la comunicación y coordinación entre un servidor central de control y múltiples semáforos inteligentes distribuidos en la ciudad, implementando conceptos avanzados de concurrencia y sincronización.

##  Objetivos Académicos

Este proyecto demuestra la implementación práctica de:

- **Concurrencia y Paralelismo**: Múltiples procesos/hilos ejecutándose simultáneamente
- **Comunicación Interprocesos**: Sockets TCP para comunicación entre servidor y clientes
- **Sincronización**: Mutex, semáforos y locks para prevenir condiciones de carrera
- **Prevención de Deadlocks**: Algoritmos de ordenamiento de recursos
- **Gestión de Recursos**: Optimización del uso de CPU y memoria
- **Sistemas Distribuidos**: Arquitectura cliente-servidor con coordinación central

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│                    SERVIDOR CENTRAL SIGET                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Coordinador   │  │  Sincronizador  │  │  Monitor    │ │
│  │   de Tráfico    │  │   de Estados    │  │  del Sistema│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────▼───┐ ┌───▼───┐ ┌───▼───┐
            │Semáforo 1 │ │Semáforo│ │Semáforo│
            │(Centro)   │ │   2    │ │   3    │
            └───────────┘ └────────┘ └────────┘
```

### Flujo de Comunicación

1. **Registro**: Los semáforos se conectan al servidor central
2. **Sincronización**: El servidor coordina los cambios de estado
3. **Monitoreo**: Supervisión continua del estado del sistema
4. **Emergencia**: Capacidad de override para situaciones críticas

##  Características Técnicas

### Mecanismos de Concurrencia

- **Threading**: Múltiples hilos para manejo concurrente de clientes
- **Locks Reentrantes**: Prevención de deadlocks en operaciones anidadas
- **Semáforos**: Control de acceso a recursos compartidos
- **Colas Thread-Safe**: Comunicación asíncrona entre componentes

### Prevención de Deadlocks

```python
def acquire_locks_in_order(self, lock_names):
    """
    Implementa prevención de deadlocks por ordenamiento de recursos
    """
    sorted_locks = sorted(lock_names, key=lambda x: self.resource_order.index(x))
    # Adquisición ordenada de recursos
```

### Sincronización de Estados

- **Mutex por Semáforo**: Cada semáforo tiene su propio lock
- **Sincronización Global**: Coordinación entre todos los semáforos
- **Heartbeat System**: Monitoreo de conectividad en tiempo real

## 🛠️ Instalación y Configuración

### Requisitos del Sistema

- Python 3.8 o superior
- Sistema operativo Windows/Linux/macOS
- Mínimo 4GB RAM
- Puerto 8888 disponible

### Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/Voinich26/siget-sistema-trafico
cd siget-sistema-trafico
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar el sistema**:
```bash
python main.py
```
#py main.py (Segun sea tu caso)

### Modos de Ejecución

```bash
# Modo interfaz gráfica (por defecto)
python main.py --mode gui

# Solo servidor
python main.py --mode server --port 8888

# Solo cliente (semáforo de prueba)
python main.py --mode client

# Con logging detallado
python main.py --log-level DEBUG
```

## 🎮 Uso del Sistema

### Interfaz Gráfica

La interfaz gráfica moderna incluye:

- **Panel de Control**: Botones para iniciar/detener el sistema
- **Visualización de Semáforos**: Representación gráfica en tiempo real
- **Panel de Logs**: Monitoreo del comportamiento concurrente
- **Estadísticas**: Métricas del sistema en tiempo real

### Controles Disponibles

- **Iniciar Sistema**: Activa el servidor y los semáforos
- **Detener Sistema**: Para todos los procesos de forma segura
- **Modo Emergencia**: Activa override de todos los semáforos
- **Sincronizar**: Fuerza sincronización manual

## 📊 Análisis de Concurrencia

### Problemas de Concurrencia Identificados

1. **Condiciones de Carrera**:
   - **Problema**: Múltiples hilos modificando el estado simultáneamente
   - **Solución**: Mutex individual por semáforo + locks reentrantes

2. **Deadlocks**:
   - **Problema**: Adquisición circular de recursos
   - **Solución**: Ordenamiento fijo de recursos + timeouts

3. **Comunicación Asíncrona**:
   - **Problema**: Mensajes perdidos o duplicados
   - **Solución**: Colas thread-safe + confirmaciones

### Mecanismos de Sincronización Implementados

```python
# Mutex para proteger estado individual
self.state_lock = threading.Lock()

# Lock reentrante para operaciones complejas
self.clients_lock = threading.RLock()

# Semáforo para control de concurrencia
self.sync_semaphore = threading.Semaphore(MAX_SEMAPHORES)

# Cola thread-safe para mensajes
self.message_queue = Queue()
```

## 🔍 Logging y Monitoreo

### Sistema de Logging Avanzado

El sistema incluye logging detallado que muestra:

- **Operaciones Concurrentes**: Qué hilo ejecuta qué operación
- **Cambios de Estado**: Transiciones de estados de semáforos
- **Sincronización**: Adquisición y liberación de recursos
- **Comunicación**: Mensajes enviados/recibidos entre procesos
- **Prevención de Deadlocks**: Cuándo y cómo se previenen

### Archivos de Log

- `logs/system.log`: Log principal del sistema
- `logs/server.log`: Actividad del servidor central
- `logs/traffic_lights.log`: Comportamiento de semáforos
- `logs/gui.log`: Interacciones de la interfaz gráfica

## 📈 Métricas de Rendimiento

### Indicadores Monitoreados

- **Clientes Conectados**: Número de semáforos activos
- **Mensajes Procesados**: Throughput de comunicación
- **Sincronizaciones**: Frecuencia de coordinación
- **Tiempo de Respuesta**: Latencia del sistema
- **Uso de Recursos**: CPU y memoria por componente

## 🧪 Casos de Prueba

### Escenarios de Prueba

1. **Inicio Normal**: Sistema arranca correctamente
2. **Conexión Múltiple**: Múltiples semáforos se conectan
3. **Sincronización**: Estados se sincronizan correctamente
4. **Modo Emergencia**: Override funciona correctamente
5. **Desconexión**: Clientes se desconectan limpiamente
6. **Recuperación**: Sistema se recupera de errores

### Comandos de Prueba

```bash
# Ejecutar con logging detallado
python main.py --log-level DEBUG

# Probar solo servidor
python main.py --mode server

# Probar solo cliente
python main.py --mode client
```

## 🔧 Configuración Avanzada

### Parámetros del Sistema

```python
# Configuración de red
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
MAX_CONNECTIONS = 10

# Configuración de semáforos
STATE_DURATIONS = {
    'RED': 8,      # 8 segundos en rojo
    'YELLOW': 3,   # 3 segundos en amarillo
    'GREEN': 10    # 10 segundos en verde
}

# Configuración de concurrencia
MAX_SEMAPHORES = 5
SYNC_TIMEOUT = 30
```

## 🎨 Diseño Visual

### Paleta de Colores (Material Design)

- **Fondo Principal**: `#1a1a1a` (Negro elegante)
- **Superficie**: `#2d2d2d` (Gris oscuro)
- **Primario**: `#2196F3` (Azul vibrante)
- **Éxito**: `#4CAF50` (Verde)
- **Error**: `#F44336` (Rojo)
- **Advertencia**: `#FFC107` (Amarillo)

### Características de la UI

- **Diseño Responsivo**: Se adapta a diferentes tamaños de ventana
- **Animaciones Suaves**: Transiciones fluidas entre estados
- **Feedback Visual**: Indicadores claros del estado del sistema
- **Tema Oscuro**: Reducción de fatiga visual

## 📚 Teoría Aplicada

### Relación con Sistemas Operativos

Este proyecto demuestra conceptos fundamentales de SO:

1. **Gestión de Procesos**: Múltiples procesos concurrentes
2. **Sincronización**: Coordinación entre procesos
3. **Comunicación Interprocesos**: Sockets y mensajes
4. **Gestión de Memoria**: Alocación eficiente de recursos
5. **Sistemas de Archivos**: Logging persistente

### Prevención del Colapso del Sistema

El sistema implementa múltiples mecanismos para prevenir el colapso:

- **Timeouts**: Evita bloqueos indefinidos
- **Heartbeat**: Detecta procesos inactivos
- **Recovery**: Recuperación automática de errores
- **Resource Management**: Liberación ordenada de recursos

## 🚀 Optimización de Rendimiento

### Estrategias Implementadas

1. **Pool de Hilos**: Reutilización de hilos para clientes
2. **Buffering**: Almacenamiento temporal de mensajes
3. **Batching**: Procesamiento por lotes de operaciones
4. **Caching**: Almacenamiento de estados frecuentemente accedidos

## 🔮 Extensiones Futuras

### Mejoras Propuestas

- **Machine Learning**: Predicción de patrones de tráfico
- **IoT Integration**: Sensores de tráfico en tiempo real
- **Mobile App**: Aplicación móvil para monitoreo
- **Cloud Deployment**: Despliegue en la nube
- **Analytics**: Análisis avanzado de datos de tráfico

## 👥 Contribuciones

### Cómo Contribuir

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Crear Pull Request con descripción detallada

### Estándares de Código

- **PEP 8**: Estilo de código Python
- **Docstrings**: Documentación de funciones
- **Type Hints**: Tipado estático
- **Logging**: Logging detallado de operaciones

## 📄 Licencia

Este proyecto es desarrollado con fines académicos. Ver `LICENSE` para más detalles.

## 📞 Contacto

- **Autor**: Angel E. Gonzalez
- **Email**: angel.guiral708@pascualbravo.edu.co
- **Curso**: Concurrencia en Sistemas Operativos
- **Universidad**: Pascual Bravo


---

**SIGET - Demostrando la potencia de la concurrencia en sistemas reales** 🚦✨
