"""
Configuración del sistema SIGET
Define constantes y parámetros del sistema de tráfico urbano
"""

# Configuración de red
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
MAX_CONNECTIONS = 10

# Configuración de semáforos
TRAFFIC_LIGHT_STATES = {
    'RED': 0,
    'YELLOW': 1, 
    'GREEN': 2
}

# Tiempos de duración de cada estado (en segundos)
STATE_DURATIONS = {
    'RED': 8,
    'YELLOW': 3,
    'GREEN': 10
}

# Configuración de concurrencia
MAX_SEMAPHORES = 5
SYNC_TIMEOUT = 30

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configuración de interfaz gráfica
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
UPDATE_INTERVAL = 100  # ms

# Colores modernos (Material Design)
COLORS = {
    'background': '#1a1a1a',
    'surface': '#2d2d2d',
    'primary': '#2196F3',
    'secondary': '#FF9800',
    'success': '#4CAF50',
    'error': '#F44336',
    'warning': '#FFC107',
    'text_primary': '#ffffff',
    'text_secondary': '#b3b3b3',
    'red_light': '#F44336',
    'yellow_light': '#FFC107',
    'green_light': '#4CAF50',
    'gray_light': '#757575'
}
