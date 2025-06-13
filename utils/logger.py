"""
Utilidades para el registro (logging) de la aplicación.

Este módulo configura el sistema de registro para la aplicación,
permitiendo registrar eventos, errores y acciones importantes.
"""

import os
import logging
from datetime import datetime
from pathlib import Path


def setup_logger():
    """Configura el sistema de registro de la aplicación.

    Returns:
        logging.Logger: Logger configurado
    """
    # Crear el directorio de logs si no existe
    log_dir = _get_log_dir()
    os.makedirs(log_dir, exist_ok=True)
    
    # Nombre del archivo de log con fecha
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f"energypy_{today}.log")
    
    # Configurar el logger principal
    logger = logging.getLogger('energypy')
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    return logger


def _get_log_dir():
    """Obtiene el directorio para los archivos de log según el sistema operativo.

    Returns:
        str: Ruta al directorio de logs
    """
    home = Path.home()
    
    if os.name == 'nt':  # Windows
        log_dir = os.path.join(home, 'AppData', 'Local', 'EnergyPy', 'logs')
    else:  # Linux/macOS
        log_dir = os.path.join(home, '.local', 'share', 'energypy', 'logs')
        
    return log_dir


def get_logger(name):
    """Obtiene un logger específico para un módulo.

    Args:
        name (str): Nombre del módulo

    Returns:
        logging.Logger: Logger configurado para el módulo
    """
    return logging.getLogger(f"energypy.{name}")


def log_action(action, details=None):
    """Registra una acción del usuario.

    Args:
        action (str): Acción realizada
        details (dict, optional): Detalles adicionales
    """
    logger = logging.getLogger('energypy.actions')
    if details:
        logger.info(f"ACTION: {action} - {details}")
    else:
        logger.info(f"ACTION: {action}")


def log_error(error, context=None):
    """Registra un error de la aplicación.

    Args:
        error (Exception): Excepción o error
        context (str, optional): Contexto donde ocurrió el error
    """
    logger = logging.getLogger('energypy.errors')
    if context:
        logger.error(f"ERROR in {context}: {str(error)}")
    else:
        logger.error(f"ERROR: {str(error)}")


def log_system_action(action_type, scheduled_time, success):
    """Registra una acción del sistema (apagado/reinicio).

    Args:
        action_type (str): Tipo de acción ('shutdown' o 'restart')
        scheduled_time (datetime): Hora programada
        success (bool): Si la acción se programó correctamente
    """
    logger = logging.getLogger('energypy.system')
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"SYSTEM ACTION: {action_type} scheduled for {scheduled_time} - {status}"
    )


def clean_old_logs(days=30):
    """Elimina logs antiguos para ahorrar espacio.

    Args:
        days (int): Número de días a mantener

    Returns:
        int: Número de archivos eliminados
    """
    log_dir = _get_log_dir()
    if not os.path.exists(log_dir):
        return 0
    
    now = datetime.now()
    deleted = 0
    
    for file in os.listdir(log_dir):
        if not file.endswith('.log'):
            continue
        
        file_path = os.path.join(log_dir, file)
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Calcular la diferencia en días
        delta = now - file_time
        if delta.days > days:
            try:
                os.remove(file_path)
                deleted += 1
            except Exception as e:
                logging.getLogger('energypy').error(
                    f"Error al eliminar log antiguo {file}: {str(e)}"
                )
    
    return deleted