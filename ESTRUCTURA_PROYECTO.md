# Estructura del Proyecto SIGET

## 📁 Organización de Archivos

```
IMPLEMENTACION DE CONCURRENCIA EN MODULOS/
├── 📄 main.py                          # Punto de entrada principal
├── 📄 run_demo.py                      # Script de demostración
├── 📄 requirements.txt                 # Dependencias del proyecto
├── 📄 LICENSE                          # Licencia MIT
├── 📄 .gitignore                       # Archivos ignorados por Git
├── 📄 README.md                        # Documentación principal
├── 📄 RELATORIA_TECNICA.md             # Relatoría técnica académica
├── 📄 ESTRUCTURA_PROYECTO.md           # Este archivo
│
├── 📁 src/                             # Código fuente principal
│   ├── 📄 __init__.py                  # Módulo principal
│   ├── 📄 config.py                    # Configuración del sistema
│   ├── 📄 traffic_light.py             # Cliente semáforo inteligente
│   ├── 📄 traffic_server.py            # Servidor central
│   ├── 📄 gui.py                       # Interfaz gráfica moderna
│   └── 📄 logger.py                    # Sistema de logging avanzado
│
├── 📁 tests/                           # Tests unitarios
│   ├── 📄 __init__.py                  # Módulo de tests
│   └── 📄 test_traffic_light.py        # Tests de concurrencia
│
├── 📁 docs/                            # Documentación adicional
│   ├── 📄 INSTALACION.md               # Guía de instalación
│   └── 📄 ARQUITECTURA.md              # Documentación de arquitectura
│
└── 📁 logs/                            # Archivos de log (se crea automáticamente)
    ├── 📄 system.log                   # Log principal del sistema
    ├── 📄 server.log                   # Log del servidor central
    ├── 📄 traffic_lights.log           # Log de semáforos
    └── 📄 gui.log                      # Log de la interfaz gráfica
```

## 🚀 Archivos Principales

### 1. **main.py** - Punto de Entrada
- **Propósito**: Ejecuta el sistema SIGET
- **Características**: 
  - Múltiples modos de ejecución (GUI, servidor, cliente)
  - Configuración de logging
  - Manejo de argumentos de línea de comandos

### 2. **src/traffic_server.py** - Servidor Central
- **Propósito**: Coordina múltiples semáforos
- **Características**:
  - Comunicación TCP/IP
  - Sincronización de estados
  - Prevención de deadlocks
  - Monitoreo del sistema

### 3. **src/traffic_light.py** - Semáforo Inteligente
- **Propósito**: Cliente semáforo con estados
- **Características**:
  - Ciclos de estados (ROJO → VERDE → AMARILLO)
  - Comunicación con servidor
  - Threading para concurrencia
  - Sincronización thread-safe

### 4. **src/gui.py** - Interfaz Gráfica
- **Propósito**: Visualización moderna del sistema
- **Características**:
  - Diseño Material Design
  - Animaciones en tiempo real
  - Panel de control interactivo
  - Logs en vivo

### 5. **src/config.py** - Configuración
- **Propósito**: Parámetros del sistema
- **Características**:
  - Configuración de red
  - Duraciones de estados
  - Colores de la interfaz
  - Parámetros de concurrencia

## 🧪 Archivos de Testing

### **tests/test_traffic_light.py**
- Tests unitarios para concurrencia
- Verificación de thread-safety
- Tests de prevención de deadlocks
- Validación de sincronización

## 📚 Documentación

### **README.md**
- Descripción completa del proyecto
- Instrucciones de instalación
- Guía de uso
- Análisis técnico

### **RELATORIA_TECNICA.md**
- Relatoría académica (2 páginas)
- Análisis de concurrencia
- Relación con teoría de SO
- Reflexión crítica

### **docs/INSTALACION.md**
- Guía detallada de instalación
- Solución de problemas
- Configuración avanzada

### **docs/ARQUITECTURA.md**
- Documentación técnica de arquitectura
- Diagramas del sistema
- Patrones de diseño
- Consideraciones de rendimiento

## 🔧 Archivos de Configuración

### **requirements.txt**
- Dependencias de Python
- Versiones específicas
- Compatibilidad

### **.gitignore**
- Archivos ignorados por Git
- Logs y archivos temporales
- Entornos virtuales

### **LICENSE**
- Licencia MIT
- Uso académico y comercial

## 🎯 Características del Proyecto

### ✅ Requisitos Académicos Cumplidos

1. **Concurrencia**: Múltiples procesos/hilos concurrentes
2. **Comunicación Interprocesos**: Sockets TCP
3. **Sincronización**: Mutex, semáforos, locks
4. **Prevención de Deadlocks**: Algoritmos de ordenamiento
5. **Interfaz Gráfica**: Tkinter con diseño moderno
6. **Logging Detallado**: Comportamiento concurrente visible
7. **Documentación Completa**: README y relatoría técnica

### 🚦 Funcionalidades del Sistema

- **6 Semáforos Inteligentes**: Distribuidos en intersecciones
- **Servidor Central**: Coordinación en tiempo real
- **Interfaz Moderna**: Material Design con animaciones
- **Modo Emergencia**: Override de todos los semáforos
- **Sincronización**: Coordinación automática de estados
- **Monitoreo**: Estadísticas y logs en tiempo real

### 🔬 Conceptos de Concurrencia Demostrados

- **Threading**: Múltiples hilos ejecutándose simultáneamente
- **Mutex**: Exclusión mutua para proteger recursos
- **Semáforos**: Control de acceso a recursos compartidos
- **Locks Reentrantes**: Prevención de deadlocks
- **Colas Thread-Safe**: Comunicación asíncrona
- **Timeouts**: Prevención de bloqueos indefinidos

## 🚀 Cómo Ejecutar

### Instalación Rápida
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar demostración
python run_demo.py
```

### Modos de Ejecución
```bash
# Interfaz gráfica (recomendado)
python main.py

# Solo servidor
python main.py --mode server

# Solo cliente
python main.py --mode client

# Con logging detallado
python main.py --log-level DEBUG
```

## 📊 Métricas del Proyecto

- **Líneas de Código**: ~2,500 líneas
- **Archivos Python**: 8 archivos
- **Tests**: 15+ casos de prueba
- **Documentación**: 4 archivos MD
- **Tiempo de Desarrollo**: Proyecto completo
- **Complejidad**: Sistema distribuido realista

## 🎓 Valor Académico

Este proyecto demuestra de manera práctica:

1. **Teoría de Concurrencia**: Aplicación real de conceptos
2. **Sistemas Distribuidos**: Comunicación cliente-servidor
3. **Gestión de Recursos**: Optimización de CPU y memoria
4. **Prevención de Fallos**: Robustez y recuperación
5. **Interfaz de Usuario**: Visualización de sistemas complejos

## 🔮 Extensiones Futuras

- **Machine Learning**: Predicción de patrones de tráfico
- **IoT Integration**: Sensores de tráfico reales
- **Mobile App**: Aplicación móvil para monitoreo
- **Cloud Deployment**: Despliegue en la nube
- **Analytics**: Análisis avanzado de datos

---

**SIGET - Un ejemplo completo de concurrencia en sistemas operativos** 🚦✨
