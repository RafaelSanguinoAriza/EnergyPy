"""
Utilidades para la internacionalización (i18n) de la aplicación.

Este módulo proporciona funciones para cargar y gestionar
las traducciones en diferentes idiomas.
"""

import os
import json
import logging


class I18n:
    """Clase para gestionar la internacionalización de la aplicación."""

    def __init__(self, default_language='es'):
        """Inicializa el sistema de internacionalización.

        Args:
            default_language (str): Idioma por defecto ('es' o 'en')
        """
        self.logger = logging.getLogger(__name__)
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}
        self._load_translations()

    def _load_translations(self):
        """Carga los archivos de traducción disponibles."""
        try:
            # Directorio de traducciones relativo al directorio actual
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            translations_dir = os.path.join(base_dir, 'resources', 'translations')
            
            # Cargar cada archivo de traducción
            for lang in ['es', 'en']:
                lang_file = os.path.join(translations_dir, f"{lang}.json")
                
                # Si el archivo no existe, crearlo con traducciones básicas
                if not os.path.exists(lang_file):
                    self._create_default_translation(lang_file, lang)
                
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
                    
            self.logger.info("Traducciones cargadas correctamente")
        except Exception as e:
            self.logger.error(f"Error al cargar traducciones: {str(e)}")
            # Crear traducciones por defecto en memoria
            self._create_default_translations_in_memory()

    def _create_default_translation(self, file_path, language):
        """Crea un archivo de traducción por defecto.

        Args:
            file_path (str): Ruta del archivo a crear
            language (str): Idioma ('es' o 'en')
        """
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Crear traducciones básicas según el idioma
        translations = self._get_default_translations(language)
        
        # Guardar el archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, indent=4, ensure_ascii=False)

    def _create_default_translations_in_memory(self):
        """Crea traducciones por defecto en memoria si no se pueden cargar los archivos."""
        for lang in ['es', 'en']:
            self.translations[lang] = self._get_default_translations(lang)

    def _get_default_translations(self, language):
        """Obtiene las traducciones por defecto para un idioma.

        Args:
            language (str): Idioma ('es' o 'en')

        Returns:
            dict: Diccionario con las traducciones
        """
        if language == 'es':
            return {
                "app_title": "EnergyPy - Control de Energía",
                "tab_time": "Programar por tiempo",
                "tab_exact_time": "Programar por hora",
                "action_shutdown": "Apagar",
                "action_restart": "Reiniciar",
                "time_value": "Valor",
                "time_unit": "Unidad",
                "seconds": "Segundos",
                "minutes": "Minutos",
                "hours": "Horas",
                "exact_time": "Hora exacta (HH:MM)",
                "schedule_button": "Programar",
                "cancel_button": "Cancelar",
                "theme_light": "Tema Claro",
                "theme_dark": "Tema Oscuro",
                "remaining_time": "Tiempo restante",
                "confirm_title": "Confirmar acción",
                "confirm_message": "¿Está seguro que desea {action} el sistema en {time}?",
                "yes": "Sí",
                "no": "No",
                "error": "Error",
                "success": "Éxito",
                "action_scheduled": "{action} programado para {time}",
                "action_cancelled": "Acción cancelada",
                "invalid_input": "Entrada inválida",
                "help": "Ayuda",
                "about": "Acerca de",
                "settings": "Configuración",
                "language": "Idioma",
                "notifications": "Notificaciones",
                "minimize_to_tray": "Minimizar a la bandeja",
                "start_minimized": "Iniciar minimizado",
                "keyboard_shortcuts": "Atajos de teclado",
                "save": "Guardar",
                "reset": "Restablecer",
                "admin_required": "Se requieren permisos de administrador",
                "admin_message": "Esta acción requiere permisos de administrador"
            }
        else:  # English
            return {
                "app_title": "EnergyPy - Power Control",
                "tab_time": "Schedule by time",
                "tab_exact_time": "Schedule by hour",
                "action_shutdown": "Shutdown",
                "action_restart": "Restart",
                "time_value": "Value",
                "time_unit": "Unit",
                "seconds": "Seconds",
                "minutes": "Minutes",
                "hours": "Hours",
                "exact_time": "Exact time (HH:MM)",
                "schedule_button": "Schedule",
                "cancel_button": "Cancel",
                "theme_light": "Light Theme",
                "theme_dark": "Dark Theme",
                "remaining_time": "Remaining time",
                "confirm_title": "Confirm action",
                "confirm_message": "Are you sure you want to {action} the system in {time}?",
                "yes": "Yes",
                "no": "No",
                "error": "Error",
                "success": "Success",
                "action_scheduled": "{action} scheduled for {time}",
                "action_cancelled": "Action cancelled",
                "invalid_input": "Invalid input",
                "help": "Help",
                "about": "About",
                "settings": "Settings",
                "language": "Language",
                "notifications": "Notifications",
                "minimize_to_tray": "Minimize to tray",
                "start_minimized": "Start minimized",
                "keyboard_shortcuts": "Keyboard shortcuts",
                "save": "Save",
                "reset": "Reset",
                "admin_required": "Administrator permissions required",
                "admin_message": "This action requires administrator permissions"
            }

    def set_language(self, language):
        """Establece el idioma actual.

        Args:
            language (str): Idioma a establecer ('es' o 'en')

        Returns:
            bool: True si se cambió correctamente, False en caso contrario
        """
        if language in self.translations:
            self.current_language = language
            return True
        return False

    def get_text(self, key, **kwargs):
        """Obtiene un texto traducido.

        Args:
            key (str): Clave del texto a traducir
            **kwargs: Variables para formatear en el texto

        Returns:
            str: Texto traducido
        """
        # Obtener el diccionario del idioma actual o el predeterminado
        lang_dict = self.translations.get(
            self.current_language,
            self.translations.get(self.default_language, {})
        )
        
        # Obtener el texto o la clave si no existe
        text = lang_dict.get(key, key)
        
        # Formatear el texto si hay variables
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError as e:
                self.logger.error(f"Error al formatear texto '{key}': {str(e)}")
                return text
        
        return text

    def get_available_languages(self):
        """Obtiene los idiomas disponibles.

        Returns:
            list: Lista de idiomas disponibles
        """
        return list(self.translations.keys())

    def get_language_name(self, language_code):
        """Obtiene el nombre del idioma a partir de su código.

        Args:
            language_code (str): Código del idioma ('es' o 'en')

        Returns:
            str: Nombre del idioma
        """
        names = {
            'es': 'Español',
            'en': 'English'
        }
        return names.get(language_code, language_code)