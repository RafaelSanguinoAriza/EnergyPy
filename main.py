"""
Punto de entrada principal para la aplicación EnergyPy.

Este script inicia la aplicación y configura el entorno necesario.
"""

import sys
import os
import platform
import logging
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Asegurar que los módulos de la aplicación sean encontrados
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController
from utils.logger import setup_logger
from utils.paths import get_resource_path

def setup_high_dpi():
    """Configura el soporte de alta resolución DPI."""
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # En macOS, el escalado DPI se maneja automáticamente
    if platform.system() == 'Windows':
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

def handle_exception(exc_type, exc_value, exc_traceback):
    """Manejador global de excepciones no capturadas."""
    # Ignorar KeyboardInterrupt
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Registrar la excepción
    logger = logging.getLogger('EnergyPy')
    logger.critical("Excepción no capturada:", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Mostrar mensaje de error al usuario
    error_msg = f"Se ha producido un error inesperado:\n{exc_value}"
    QMessageBox.critical(None, "Error crítico", error_msg)

def main():
    """Función principal que inicia la aplicación."""
    # Configurar el manejador de excepciones
    sys.excepthook = handle_exception
    
    # Configurar el logger
    setup_logger()
    logger = logging.getLogger('EnergyPy')
    logger.info(f"Iniciando EnergyPy en {platform.system()} {platform.release()}")
    
    # Configurar DPI antes de crear la aplicación
    setup_high_dpi()
    
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName("EnergyPy")
    app.setOrganizationName("EnergyPy")
    
    # Configurar el icono de la aplicación según la plataforma
    icon_filename = ""
    if platform.system() == "Windows":
        icon_filename = "icon.ico"
    elif platform.system() == "Darwin":  # macOS
        icon_filename = "icon.icns"
    else:  # Linux y otros
        icon_filename = "icon.png"
    
    icon_path = get_resource_path(icon_filename)
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        logger.info(f"Icono cargado desde: {icon_path}")
    else:
        logger.warning(f"No se pudo encontrar el icono en: {icon_path}")
    
    # Iniciar el controlador principal
    controller = MainController()
    controller.start()
    
    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()