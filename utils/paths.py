"""Utilidades para el manejo de rutas multiplataforma."""

import os
import sys
import platform

def get_app_dir():
    """
    Obtiene el directorio base de la aplicación de manera multiplataforma.
    """
    if getattr(sys, 'frozen', False):
        # Ejecutando como ejecutable compilado
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_dir():
    """
    Obtiene el directorio de configuración específico de la plataforma.
    """
    system = platform.system()
    app_name = "EnergyPy"
    
    if system == "Windows":
        base_dir = os.path.join(os.environ["APPDATA"], app_name)
    elif system == "Darwin":
        base_dir = os.path.expanduser(f"~/Library/Application Support/{app_name}")
    else:  # Linux y otros
        base_dir = os.path.expanduser(f"~/.config/{app_name}")
    
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def get_resource_path(relative_path):
    """
    Obtiene la ruta absoluta a un recurso, funcionando tanto en desarrollo como en producción.
    
    Args:
        relative_path: Ruta relativa al archivo de recurso dentro de la carpeta resources
        
    Returns:
        Ruta absoluta al recurso
    """
    # Cuando se ejecuta como aplicación empaquetada con PyInstaller
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        return os.path.join(sys._MEIPASS, 'resources', relative_path)
    
    # En desarrollo
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, 'resources', relative_path)