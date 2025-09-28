#!/usr/bin/env python3
"""
SIGET - Sistema de Gestión de Tráfico Urbano
Proyecto académico de concurrencia en sistemas operativos

Autor: [Tu Nombre]
Curso: Concurrencia en Sistemas Operativos
Fecha: 2024

Este proyecto implementa un sistema distribuido de semáforos inteligentes
que se comunican con un servidor central, demostrando conceptos de:
- Concurrencia y paralelismo
- Sincronización entre procesos
- Prevención de deadlocks
- Comunicación interprocesos
- Gestión de recursos del sistema operativo
"""

import sys
import os
import logging
import argparse
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import *
from src.gui import SIGETGUI

def setup_logging(log_level='INFO'):
    """Configura el sistema de logging para el proyecto"""
    # Crear directorio de logs si no existe
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_dir / 'siget.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Logger principal
    logger = logging.getLogger('SIGET')
    logger.info("=== SIGET - Sistema de Gestión de Tráfico Urbano ===")
    logger.info("Iniciando sistema con logging configurado")
    
    return logger

def print_banner():
    """Imprime el banner del sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    SIGET - Sistema de Gestión de Tráfico Urbano             ║
    ║                                                              ║
    ║    Proyecto Académico de Concurrencia en Sistemas Operativos ║
    ║                                                              ║
    ║    Características:                                          ║
    ║    • Sistema distribuido con comunicación por sockets        ║
    ║    • Concurrencia y sincronización entre procesos           ║
    ║    • Prevención de deadlocks y condiciones de carrera       ║
    ║    • Interfaz gráfica moderna y responsiva                  ║
    ║    • Logging detallado del comportamiento concurrente       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Función principal del sistema SIGET"""
    # Importar configuración por defecto
    from src.config import LOG_LEVEL as DEFAULT_LOG_LEVEL, SERVER_PORT as DEFAULT_SERVER_PORT, SERVER_HOST as DEFAULT_SERVER_HOST
    
    parser = argparse.ArgumentParser(description='SIGET - Sistema de Gestión de Tráfico Urbano')
    parser.add_argument('--mode', choices=['gui', 'server', 'client'], default='gui',
                       help='Modo de ejecución del sistema')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default=DEFAULT_LOG_LEVEL, help='Nivel de logging')
    parser.add_argument('--port', type=int, default=DEFAULT_SERVER_PORT, 
                       help='Puerto del servidor')
    parser.add_argument('--host', default=DEFAULT_SERVER_HOST, 
                       help='Host del servidor')
    
    args = parser.parse_args()
    
    # Usar valores de los argumentos
    log_level = args.log_level
    server_port = args.port
    server_host = args.host
    
    # Configurar logging
    logger = setup_logging(log_level)
    
    # Imprimir banner
    print_banner()
    
    try:
        if args.mode == 'gui':
            # Modo interfaz gráfica (por defecto)
            logger.info("Iniciando en modo interfaz gráfica")
            app = SIGETGUI()
            app.run()
            
        elif args.mode == 'server':
            # Modo solo servidor
            logger.info("Iniciando solo servidor")
            from src.traffic_server import TrafficServer
            
            server = TrafficServer()
            if server.start_server():
                logger.info("Servidor iniciado correctamente")
                try:
                    # Mantener el servidor ejecutándose
                    while True:
                        import time
                        time.sleep(1)
                except KeyboardInterrupt:
                    logger.info("Deteniendo servidor...")
                    server.stop_server()
            else:
                logger.error("No se pudo iniciar el servidor")
                sys.exit(1)
                
        elif args.mode == 'client':
            # Modo solo cliente (semáforo)
            logger.info("Iniciando solo cliente")
            from src.traffic_light import TrafficLight
            
            # Crear un semáforo de prueba
            traffic_light = TrafficLight("TEST001", "Intersección de Prueba", 0, 0)
            if traffic_light.start():
                logger.info("Semáforo iniciado correctamente")
                try:
                    # Mantener el semáforo ejecutándose
                    while True:
                        import time
                        time.sleep(1)
                except KeyboardInterrupt:
                    logger.info("Deteniendo semáforo...")
                    traffic_light.stop()
            else:
                logger.error("No se pudo iniciar el semáforo")
                sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error crítico en el sistema: {e}")
        sys.exit(1)
    
    logger.info("Sistema SIGET finalizado")

if __name__ == "__main__":
    main()
