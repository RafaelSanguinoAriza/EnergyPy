"""
Modelo para la gestión del sistema operativo y operaciones de apagado/reinicio.

Este módulo proporciona una abstracción para detectar el sistema operativo
y ejecutar comandos nativos para apagar o reiniciar el sistema.
"""

import os
import sys
import platform
import logging
import subprocess
from datetime import datetime, timedelta


class SystemModel:
    """Modelo para gestionar operaciones del sistema operativo."""

    def __init__(self):
        """Inicializa el modelo del sistema."""
        self.os_type = platform.system().lower()
        self.logger = logging.getLogger(__name__)
        self.scheduled_action = None
        self.scheduled_time = None
        self.action_type = None  # 'shutdown' o 'restart'

    def get_os_type(self):
        """Retorna el tipo de sistema operativo."""
        return self.os_type

    def requires_admin(self):
        """Verifica si se requieren permisos de administrador."""
        if self.os_type == 'windows':
            import ctypes
            return not ctypes.windll.shell32.IsUserAnAdmin()
        elif self.os_type in ['linux', 'darwin']:
            return os.geteuid() != 0
        return False

    def schedule_shutdown(self, seconds=0, action_type='shutdown'):
        """Programa el apagado del sistema.

        Args:
            seconds (int): Segundos hasta el apagado
            action_type (str): 'shutdown' o 'restart'

        Returns:
            bool: True si se programó correctamente, False en caso contrario
        """
        try:
            self.scheduled_time = datetime.now() + timedelta(seconds=seconds)
            self.action_type = action_type

            if self.os_type == 'windows':
                cmd = 'shutdown'
                flag = '/s' if action_type == 'shutdown' else '/r'
                args = [cmd, flag, '/t', str(seconds)]
            elif self.os_type == 'linux':
                cmd = 'shutdown'
                flag = '-h' if action_type == 'shutdown' else '-r'
                args = [cmd, flag, f'+{seconds // 60}']
            elif self.os_type == 'darwin':  # macOS
                cmd = 'shutdown'
                flag = '-h' if action_type == 'shutdown' else '-r'
                args = [cmd, flag, f'+{seconds // 60}']
            else:
                self.logger.error(f"Sistema operativo no soportado: {self.os_type}")
                return False

            self.scheduled_action = subprocess.Popen(args)
            self.logger.info(f"Programado {action_type} para {self.scheduled_time}")
            return True
        except Exception as e:
            self.logger.error(f"Error al programar {action_type}: {str(e)}")
            return False

    def schedule_shutdown_at_time(self, target_time, action_type='shutdown'):
        """Programa el apagado a una hora específica.

        Args:
            target_time (datetime): Hora objetivo para el apagado
            action_type (str): 'shutdown' o 'restart'

        Returns:
            bool: True si se programó correctamente, False en caso contrario
        """
        now = datetime.now()
        if target_time <= now:
            # Si la hora es en el pasado, asumimos que es para mañana
            target_time = target_time.replace(day=now.day + 1)

        seconds = int((target_time - now).total_seconds())
        return self.schedule_shutdown(seconds, action_type)

    def cancel_scheduled_action(self):
        """Cancela cualquier apagado o reinicio programado.

        Returns:
            bool: True si se canceló correctamente, False en caso contrario
        """
        try:
            if self.os_type == 'windows':
                subprocess.run(['shutdown', '/a'])
            elif self.os_type in ['linux', 'darwin']:
                subprocess.run(['shutdown', '-c'])
            else:
                self.logger.error(f"Sistema operativo no soportado: {self.os_type}")
                return False

            self.scheduled_action = None
            self.scheduled_time = None
            self.action_type = None
            self.logger.info("Acción programada cancelada")
            return True
        except Exception as e:
            self.logger.error(f"Error al cancelar acción programada: {str(e)}")
            return False

    def get_remaining_time(self):
        """Obtiene el tiempo restante hasta la acción programada.

        Returns:
            int: Segundos restantes o None si no hay acción programada
        """
        if self.scheduled_time is None:
            return None

        remaining = (self.scheduled_time - datetime.now()).total_seconds()
        return max(0, int(remaining))

    def get_scheduled_info(self):
        """Obtiene información sobre la acción programada.

        Returns:
            dict: Información de la acción programada o None si no hay
        """
        if self.scheduled_time is None:
            return None

        return {
            'action_type': self.action_type,
            'scheduled_time': self.scheduled_time,
            'remaining_seconds': self.get_remaining_time()
        }