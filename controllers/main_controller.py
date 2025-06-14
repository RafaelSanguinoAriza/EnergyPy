"""
Controlador principal de la aplicación EnergyPy.

Este módulo conecta los modelos con las vistas y maneja la lógica de la aplicación.
"""

import os
import sys
import logging
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMessageBox, QAction
from PyQt5.QtCore import QTimer

from models.system_model import SystemModel
from models.config_model import ConfigModel
from views.main_view import MainView
from views.settings_view import SettingsView
from views.help_view import HelpView, AboutView
from utils.i18n import I18n
from utils.logger import setup_logger, log_action


class MainController:
    """Controlador principal de la aplicación."""

    def __init__(self):
        """Inicializa el controlador principal."""
        # Configurar el logger
        self.logger = setup_logger()
        self.logger.info("Iniciando aplicación EnergyPy")
        
        # Inicializar modelos
        self.system_model = SystemModel()
        self.config_model = ConfigModel()
        
        # Cargar configuración
        self.config = self.config_model.get_config()
        
        # Inicializar internacionalización
        self.i18n = I18n(self.config['language'])
        
        # Inicializar vistas
        self.main_view = None
        self.settings_view = None
        self.help_view = None
        self.about_view = None
        
        # Timer para actualizar la cuenta regresiva
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_countdown)
        self.update_timer.start(1000)  # Actualizar cada segundo
        
        # Verificar permisos de administrador
        self._check_admin_permissions()

    def start(self):
        """Inicia la aplicación y muestra la vista principal."""
        # Inicializar la vista principal
        self.main_view = MainView(self, self.i18n)
        
        # Conectar señales de la vista principal
        self._connect_main_view_signals()
        
        # Cargar tema
        self._load_theme()
        
        # Cargar configuración en la vista
        self._load_config_to_view()
        
        # Mostrar la vista principal
        if self.config['start_minimized'] and self.config['minimize_to_tray']:
            self.main_view.hide()
        else:
            self.main_view.show()
        
        self.logger.info("Aplicación iniciada correctamente")

    def _check_admin_permissions(self):
        """Verifica si la aplicación tiene permisos de administrador."""
        if self.system_model.requires_admin():
            self.logger.warning("La aplicación no tiene permisos de administrador")
            # Mostrar advertencia al usuario
            QMessageBox.warning(
                None,
                self.i18n.get_text("admin_required_title"),
                self.i18n.get_text("admin_required_message")
            )

    def _connect_main_view_signals(self):
        """Conecta las señales de la vista principal."""
        if self.main_view:
            # Botones principales
            self.main_view.schedule_button.clicked.connect(self.schedule_action)
            self.main_view.cancel_button.clicked.connect(self.cancel_action)
            
            # Cambio de tema
            self.main_view.theme_switch.stateChanged.connect(self.toggle_theme)
            
            # Añadir menú de opciones
            self._setup_menu()

    def _setup_menu(self):
        """Configura el menú de la aplicación."""
        # Obtener la barra de menú
        menubar = self.main_view.menuBar()
        
        # Limpiar la barra de menú existente
        menubar.clear()
        
        # Menú Archivo
        file_menu = menubar.addMenu(self.i18n.get_text("menu_file"))
        
        # Acción Configuración
        self.settings_action = QAction(self.i18n.get_text("settings"), self.main_view)
        self.settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(self.settings_action)
        
        file_menu.addSeparator()
        
        # Acción Salir
        self.exit_action = QAction(self.i18n.get_text("tray_exit"), self.main_view)
        self.exit_action.triggered.connect(self.exit_app)
        file_menu.addAction(self.exit_action)
        
        # Menú Ayuda
        help_menu = menubar.addMenu(self.i18n.get_text("menu_help"))
        
        # Acción Ayuda
        self.help_action = QAction(self.i18n.get_text("help"), self.main_view)
        self.help_action.triggered.connect(self.show_help)
        help_menu.addAction(self.help_action)
        
        # Acción Acerca de
        self.about_action = QAction(self.i18n.get_text("about"), self.main_view)
        self.about_action.triggered.connect(self.show_about)
        help_menu.addAction(self.about_action)

    def _load_theme(self):
        """Carga el tema de la aplicación."""
        theme = self.config['theme']
        theme_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'styles', f'{theme}.qss'
        )
        
        try:
            with open(theme_file, 'r', encoding='utf-8') as f:
                style = f.read()
                QApplication.instance().setStyleSheet(style)
                self.logger.info(f"Tema cargado: {theme}")
        except Exception as e:
            self.logger.error(f"Error al cargar el tema: {str(e)}")

    def _load_config_to_view(self):
        """Carga la configuración en la vista principal."""
        if self.main_view:
            # Establecer pestaña activa
            self.main_view.tab_widget.setCurrentIndex(self.config['last_used_tab'])
            
            # Establecer valores de tiempo
            self.main_view.time_value_spin.setValue(self.config['last_used_time_value'])
            
            # Establecer unidad de tiempo
            time_unit_index = {
                'seconds': 0,
                'minutes': 1,
                'hours': 2
            }.get(self.config['last_used_time_unit'], 1)
            self.main_view.time_unit_combo.setCurrentIndex(time_unit_index)
            
            # Establecer acción
            if self.config['last_used_action'] == 'shutdown':
                self.main_view.shutdown_radio.setChecked(True)
            else:
                self.main_view.restart_radio.setChecked(True)
            
            # Establecer tema
            self.main_view.theme_switch.setChecked(self.config['theme'] == 'dark')

    def schedule_action(self):
        """Programa una acción de apagado o reinicio."""
        # Obtener tipo de acción
        action_type = 'shutdown' if self.main_view.shutdown_radio.isChecked() else 'restart'
        
        # Guardar configuración
        self.config_model.set_config('last_used_action', action_type)
        
        # Obtener pestaña activa
        current_tab = self.main_view.tab_widget.currentIndex()
        self.config_model.set_config('last_used_tab', current_tab)
        
        success = False
        scheduled_time = None
        
        if current_tab == 0:  # Pestaña de tiempo
            # Obtener valor y unidad de tiempo
            time_value = self.main_view.time_value_spin.value()
            time_unit_index = self.main_view.time_unit_combo.currentIndex()
            time_unit = ['seconds', 'minutes', 'hours'][time_unit_index]
            
            # Guardar configuración
            self.config_model.set_config('last_used_time_value', time_value)
            self.config_model.set_config('last_used_time_unit', time_unit)
            
            # Convertir a segundos
            seconds = time_value
            if time_unit == 'minutes':
                seconds *= 60
            elif time_unit == 'hours':
                seconds *= 3600
            
            # Guardar el tiempo original en segundos para el cálculo del progreso
            self.system_model.original_seconds = seconds
            
            # Programar acción
            success = self.system_model.schedule_shutdown(seconds, action_type)
            scheduled_time = datetime.now().strftime('%H:%M:%S')
            
            log_action(f"Programado {action_type} en {time_value} {time_unit}")
            
        elif current_tab == 1:  # Pestaña de hora exacta
            # Obtener hora exacta
            target_time = self.main_view.exact_time_edit.time().toPyTime()
            target_datetime = datetime.now().replace(
                hour=target_time.hour,
                minute=target_time.minute,
                second=0,
                microsecond=0
            )
            
            # Programar acción
            success = self.system_model.schedule_shutdown_at_time(target_datetime, action_type)
            scheduled_time = target_datetime.strftime('%H:%M:%S')
            
            # Guardar el tiempo original en segundos para el cálculo del progreso
            now = datetime.now()
            seconds = int((target_datetime - now).total_seconds())
            self.system_model.original_seconds = seconds
            
            log_action(f"Programado {action_type} a las {scheduled_time}")
        
        if success:
            # Actualizar interfaz
            self.main_view.schedule_button.setEnabled(False)
            self.main_view.cancel_button.setEnabled(True)
            self.main_view.tab_widget.setEnabled(False)
            # Deshabilitar los radio buttons individualmente
            self.main_view.shutdown_radio.setEnabled(False)
            self.main_view.restart_radio.setEnabled(False)
            
            # Mostrar notificación
            if self.config['show_notifications']:
                self.main_view.tray_icon.showMessage(
                    self.i18n.get_text("app_title"),
                    self.i18n.get_text(
                        "notification_scheduled",
                        action=self.i18n.get_text(f"action_{action_type}"),
                        time=scheduled_time
                    ),
                    3000
                )
        else:
            # Mostrar error
            QMessageBox.critical(
                self.main_view,
                self.i18n.get_text("error_title"),
                self.i18n.get_text("error_scheduling")
            )

    def cancel_action(self):
        """Cancela la acción programada."""
        success = self.system_model.cancel_scheduled_action()
        
        if success:
            # Restablecer la interfaz
            self.main_view.schedule_button.setEnabled(True)
            self.main_view.cancel_button.setEnabled(False)
            self.main_view.tab_widget.setEnabled(True)
            self.main_view.shutdown_radio.setEnabled(True)
            self.main_view.restart_radio.setEnabled(True)
            
            # Restablecer barra de progreso y tiempo restante
            self.main_view.progress_bar.setValue(0)
            self.main_view.remaining_time_label.setText("--:--:--")
            
            # Restablecer el tiempo original en segundos
            self.system_model.original_seconds = 0
            
            log_action("Acción programada cancelada")
            
            # Mostrar notificación
            if self.config['show_notifications']:
                self.main_view.tray_icon.showMessage(
                    self.i18n.get_text("app_title"),
                    self.i18n.get_text("notification_cancelled"),
                    3000
                )
        else:
            # Mostrar error
            QMessageBox.critical(
                self.main_view,
                self.i18n.get_text("error_title"),
                self.i18n.get_text("error_cancelling")
            )

    def update_countdown(self):
        """Actualiza la cuenta regresiva en la interfaz."""
        if not self.main_view or not self.system_model.get_scheduled_info():
            return
        
        remaining = self.system_model.get_remaining_time()
        if remaining is not None:
            # Calcular horas, minutos y segundos
            hours, remainder = divmod(remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Actualizar etiqueta de tiempo restante
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.main_view.remaining_time_label.setText(time_str)
            
            # Obtener información de la acción programada
            info = self.system_model.get_scheduled_info()
            
            # Obtener el tiempo total original
            total_seconds = getattr(self.system_model, 'original_seconds', 0)
            
            # Actualizar barra de progreso
            if total_seconds > 0:
                # Calcular el progreso como porcentaje del tiempo transcurrido
                progress = int(((total_seconds - remaining) / total_seconds) * 100)
                self.main_view.progress_bar.setValue(progress)
            
            # Si el tiempo restante es 0, restablecer la interfaz
            if remaining == 0:
                self.main_view.schedule_button.setEnabled(True)
                self.main_view.cancel_button.setEnabled(False)
                self.main_view.tab_widget.setEnabled(True)
                self.main_view.shutdown_radio.setEnabled(True)
                self.main_view.restart_radio.setEnabled(True)
            self.main_view.tab_widget.setEnabled(True)

    def toggle_theme(self, state):
        """Cambia entre tema claro y oscuro."""
        theme = 'dark' if state else 'light'
        self.config_model.set_theme(theme)
        self._load_theme()
        log_action(f"Cambiado tema a {theme}")

    def show_settings(self):
        """Muestra la vista de configuración."""
        self.settings_view = SettingsView(self.main_view, self.i18n, self.config_model)
        self.settings_view.settings_changed.connect(self._update_config)
        self.settings_view.exec_()
        log_action("Vista de configuración mostrada")

    def _update_config(self, new_config):
        """Actualiza la configuración desde la vista de configuración.
        
        Args:
            new_config (dict): Nueva configuración
        """
        # Actualizar idioma si ha cambiado
        if new_config['language'] != self.config['language']:
            self.i18n.set_language(new_config['language'])
            self._reload_ui_texts()
        
        # Guardar configuración
        for key, value in new_config.items():
            self.config_model.set_config(key, value)
        
        # Recargar configuración
        self.config = self.config_model.get_config()
        
        log_action("Configuración actualizada")

    def _reload_ui_texts(self):
        """Recarga los textos de la interfaz tras cambio de idioma."""
        if self.main_view:
            # Actualizar los textos de la interfaz sin cerrar la vista principal
            # Actualizar el menú
            self._setup_menu()
            
            # Actualizar el icono de la bandeja del sistema
            if hasattr(self.main_view, 'tray_icon') and self.main_view.tray_icon:
                self.main_view.tray_icon.setToolTip(self.i18n.get_text("app_title"))
                
                # Actualizar el menú contextual del icono de la bandeja
                if hasattr(self.main_view, '_setup_tray_icon'):
                    self.main_view._setup_tray_icon()
            
            # Actualizar los textos de los widgets
            self.main_view.setWindowTitle(self.i18n.get_text("app_title"))
            
            # Actualizar pestañas
            self.main_view.tab_widget.setTabText(0, self.i18n.get_text("tab_time"))
            self.main_view.tab_widget.setTabText(1, self.i18n.get_text("tab_exact_time"))
            
            # Actualizar botones de acción
            self.main_view.shutdown_radio.setText(self.i18n.get_text("action_shutdown"))
            self.main_view.restart_radio.setText(self.i18n.get_text("action_restart"))
            
            # Actualizar botones principales
            self.main_view.schedule_button.setText(self.i18n.get_text("schedule_button"))
            self.main_view.cancel_button.setText(self.i18n.get_text("cancel_button"))
            
            # Actualizar la configuración en la vista
            self._load_config_to_view()

    def show_help(self):
        """Muestra la vista de ayuda."""
        # Crear una nueva instancia cada vez para evitar problemas con el objeto C/C++
        help_view = HelpView(self.main_view, self.i18n)
        help_view.show()
        # Guardar una referencia para evitar que se elimine prematuramente
        self.help_view = help_view
        log_action("Vista de ayuda mostrada")

    def show_about(self):
        """Muestra la vista de acerca de."""
        # Crear una nueva instancia cada vez para evitar problemas con el objeto C/C++
        about_view = AboutView(self.main_view, self.i18n)
        about_view.show()
        # Guardar una referencia para evitar que se elimine prematuramente
        self.about_view = about_view
        log_action("Vista de acerca de mostrada")

    def get_config(self, key=None):
        """Obtiene la configuración o un valor específico.

        Args:
            key (str, optional): Clave específica a obtener

        Returns:
            dict or any: Configuración completa o valor específico
        """
        if key is None:
            return self.config
        return self.config.get(key)

    def exit_app(self):
        """Cierra la aplicación."""
        # Cancelar cualquier acción programada
        if self.system_model.get_scheduled_info():
            self.system_model.cancel_scheduled_action()
        
        # Cerrar la aplicación
        QApplication.instance().quit()
        log_action("Aplicación cerrada")