"""
Modelo para la gestión de configuración y preferencias del usuario.

Este módulo maneja el almacenamiento y recuperación de las preferencias
del usuario, como el tema, idioma y configuraciones recientes.
"""

import os
import json
import logging
from pathlib import Path


class ConfigModel:
    """Modelo para gestionar la configuración y preferencias del usuario."""

    def __init__(self):
        """Inicializa el modelo de configuración."""
        self.logger = logging.getLogger(__name__)
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.default_config = {
            'theme': 'light',  # 'light' o 'dark'
            'language': 'es',  # 'es' o 'en'
            'last_used_tab': 0,  # 0: tiempo, 1: hora exacta
            'last_used_time_unit': 'minutes',  # 'seconds', 'minutes', 'hours'
            'last_used_time_value': 30,
            'last_used_action': 'shutdown',  # 'shutdown' o 'restart'
            'show_notifications': True,
            'minimize_to_tray': True,
            'start_minimized': False,
            'keyboard_shortcuts': {
                'cancel': 'Ctrl+C',
                'switch_tab': 'Ctrl+Tab',
                'toggle_theme': 'Ctrl+T'
            }
        }
        self.config = self._load_config()

    def _get_config_dir(self):
        """Obtiene el directorio de configuración según el sistema operativo."""
        home = Path.home()
        
        if os.name == 'nt':  # Windows
            config_dir = os.path.join(home, 'AppData', 'Local', 'EnergyPy')
        else:  # Linux/macOS
            config_dir = os.path.join(home, '.config', 'energypy')
            
        # Crear el directorio si no existe
        os.makedirs(config_dir, exist_ok=True)
        return config_dir

    def _load_config(self):
        """Carga la configuración desde el archivo o crea uno nuevo."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Asegurar que todas las claves existan
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                self._save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            self.logger.error(f"Error al cargar la configuración: {str(e)}")
            return self.default_config.copy()

    def _save_config(self, config):
        """Guarda la configuración en el archivo."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Error al guardar la configuración: {str(e)}")
            return False

    def get_config(self, key=None):
        """Obtiene toda la configuración o un valor específico.

        Args:
            key (str, optional): Clave específica a obtener

        Returns:
            dict or any: Configuración completa o valor específico
        """
        if key is None:
            return self.config
        return self.config.get(key, self.default_config.get(key))

    def set_config(self, key, value):
        """Establece un valor de configuración y lo guarda.

        Args:
            key (str): Clave a modificar
            value (any): Nuevo valor

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        self.config[key] = value
        return self._save_config(self.config)

    def reset_config(self):
        """Restablece la configuración a los valores predeterminados.

        Returns:
            bool: True si se restableció correctamente, False en caso contrario
        """
        self.config = self.default_config.copy()
        return self._save_config(self.config)

    def get_theme(self):
        """Obtiene el tema actual.

        Returns:
            str: 'light' o 'dark'
        """
        return self.config.get('theme', 'light')

    def set_theme(self, theme):
        """Establece el tema.

        Args:
            theme (str): 'light' o 'dark'

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if theme not in ['light', 'dark']:
            return False
        return self.set_config('theme', theme)

    def get_language(self):
        """Obtiene el idioma actual.

        Returns:
            str: 'es' o 'en'
        """
        return self.config.get('language', 'es')

    def set_language(self, language):
        """Establece el idioma.

        Args:
            language (str): 'es' o 'en'

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if language not in ['es', 'en']:
            return False
        return self.set_config('language', language)