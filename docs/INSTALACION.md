# Guía de Instalación - SIGET

## Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10/11, macOS 10.14+, o Linux (Ubuntu 18.04+)
- **Python**: Versión 3.8 o superior
- **Memoria RAM**: Mínimo 4GB (recomendado 8GB)
- **Espacio en Disco**: 100MB libres
- **Red**: Puerto 8888 disponible para comunicación local

### Requisitos Recomendados
- **Python**: Versión 3.9 o superior
- **Memoria RAM**: 8GB o más
- **Procesador**: Múltiples cores para mejor rendimiento concurrente
- **Pantalla**: Resolución 1920x1080 o superior para la interfaz gráfica

## Instalación Paso a Paso

### 1. Verificar Python

Abre una terminal/consola y verifica que Python esté instalado:

```bash
python --version
# o
python3 --version
```

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/siget-sistema-trafico.git
cd siget-sistema-trafico
```

### 3. Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Verificar Instalación

```bash
python main.py --help
```

## Modos de Ejecución

### Modo Interfaz Gráfica (Recomendado)

```bash
python main.py
# o
python run_demo.py
```

### Modo Solo Servidor

```bash
python main.py --mode server
```

### Modo Solo Cliente

```bash
python main.py --mode client
```

### Con Logging Detallado

```bash
python main.py --log-level DEBUG
```

## Solución de Problemas

### Error: "ModuleNotFoundError"

Si obtienes errores de módulos no encontrados:

```bash
# Verificar que estás en el directorio correcto
pwd
ls -la

# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error: "Address already in use"

Si el puerto 8888 está ocupado:

```bash
# Usar un puerto diferente
python main.py --port 8889
```

### Error: "Permission denied"

En sistemas Unix/macOS, es posible que necesites permisos de administrador:

```bash
sudo python main.py
```

### Problemas con Tkinter

Si la interfaz gráfica no se abre:

```bash
# En Ubuntu/Debian
sudo apt-get install python3-tk

# En CentOS/RHEL
sudo yum install tkinter
```

## Configuración Avanzada

### Variables de Entorno

Puedes configurar el sistema usando variables de entorno:

```bash
export SIGET_HOST=localhost
export SIGET_PORT=8888
export SIGET_LOG_LEVEL=INFO
```

### Archivo de Configuración

Edita `src/config.py` para personalizar:

```python
# Cambiar puerto del servidor
SERVER_PORT = 8888

# Cambiar duración de estados
STATE_DURATIONS = {
    'RED': 8,      # 8 segundos en rojo
    'YELLOW': 3,   # 3 segundos en amarillo
    'GREEN': 10    # 10 segundos en verde
}
```

## Verificación de la Instalación

### Test Automático

```bash
python -m pytest tests/
```

### Test Manual

1. Ejecuta el sistema: `python main.py`
2. Verifica que se abra la interfaz gráfica
3. Haz clic en "Iniciar Sistema"
4. Observa que los semáforos cambien de estado
5. Revisa los logs en el panel inferior

## Desinstalación

Para desinstalar el sistema:

```bash
# Desactivar entorno virtual
deactivate

# Eliminar directorio del proyecto
rm -rf siget-sistema-trafico
```

## Soporte

Si encuentras problemas durante la instalación:

1. Revisa los logs en `logs/siget.log`
2. Verifica que todos los requisitos estén cumplidos
3. Consulta la sección de solución de problemas
4. Crea un issue en el repositorio de GitHub
