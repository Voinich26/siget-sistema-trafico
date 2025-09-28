#!/usr/bin/env python3
"""
Script de demostración para SIGET
Ejecuta el sistema con configuración optimizada para demostración
"""

import sys
import os
import time
import threading
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def print_demo_banner():
    """Imprime el banner de demostración"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🚦 SIGET - DEMOSTRACIÓN ACADÉMICA 🚦                     ║
    ║                                                              ║
    ║    Sistema de Gestión de Tráfico Urbano                     ║
    ║    con Concurrencia y Sincronización                        ║
    ║                                                              ║
    ║    Características de la demostración:                      ║
    ║    • 6 semáforos inteligentes distribuidos                  ║
    ║    • Servidor central con coordinación en tiempo real       ║
    ║    • Interfaz gráfica moderna con animaciones               ║
    ║    • Logging detallado del comportamiento concurrente       ║
    ║    • Prevención de deadlocks y condiciones de carrera       ║
    ║                                                              ║
    ║    Presiona Ctrl+C para detener la demostración             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_demo():
    """Ejecuta la demostración del sistema"""
    print_demo_banner()
    
    # Crear directorio de logs si no existe
    Path('logs').mkdir(exist_ok=True)
    
    try:
        # Importar y ejecutar la GUI
        from src.gui import SIGETGUI
        
        print("🚀 Iniciando sistema SIGET...")
        print("📊 La interfaz gráfica se abrirá en unos segundos...")
        print("🔍 Observa los logs en tiempo real para ver el comportamiento concurrente")
        print("⚡ Usa los botones de control para interactuar con el sistema")
        print()
        
        # Crear y ejecutar la aplicación
        app = SIGETGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Demostración detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        print("💡 Asegúrate de que todas las dependencias estén instaladas")
        print("   Ejecuta: pip install -r requirements.txt")

if __name__ == "__main__":
    run_demo()
