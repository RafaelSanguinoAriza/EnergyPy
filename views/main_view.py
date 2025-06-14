"""
Vista principal de la aplicación EnergyPy.

Este módulo implementa la interfaz gráfica principal de la aplicación,
con todas las funcionalidades requeridas en la especificación.
"""

import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QRadioButton, QButtonGroup, QSpinBox,
    QComboBox, QTimeEdit, QProgressBar, QCheckBox, QSystemTrayIcon,
    QMenu, QAction, QMessageBox, QGroupBox, QFormLayout, QApplication
)
from PyQt5.QtCore import Qt, QTime, QTimer, QSize
from PyQt5.QtGui import QIcon, QPixmap

# Importar get_resource_path al inicio del archivo
from utils.paths import get_resource_path


class MainView(QMainWindow):
    """Vista principal de la aplicación."""

    def __init__(self, controller, i18n):
        """Inicializa la vista principal.

        Args:
            controller: Controlador de la aplicación
            i18n: Instancia de internacionalización
        """
        super().__init__()
        self.controller = controller
        self.i18n = i18n
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        
        # Inicializar la interfaz
        self._init_ui()
        
        # Configurar el icono de la bandeja del sistema
        self._setup_tray_icon()
        
        # Configurar atajos de teclado
        self._setup_shortcuts()

    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Configuración de la ventana principal
        self.setWindowTitle(self.i18n.get_text("app_title"))
        self.setMinimumSize(500, 400)
        
        # Cargar el icono de la aplicación usando get_resource_path
        app_icon_path = get_resource_path(os.path.join('icons', 'app_icon.svg'))
        self.setWindowIcon(QIcon(app_icon_path))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título de la aplicación
        title_label = QLabel(self.i18n.get_text("app_title"))
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Pestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Pestaña de programación por tiempo
        time_tab = QWidget()
        time_layout = QVBoxLayout(time_tab)
        
        # Grupo de configuración de tiempo
        time_group = QGroupBox(self.i18n.get_text("tab_time"))
        time_form = QFormLayout(time_group)
        
        # Valor de tiempo
        time_value_layout = QHBoxLayout()
        self.time_value_spin = QSpinBox()
        self.time_value_spin.setRange(1, 86400)  # Máximo 24 horas en segundos
        self.time_value_spin.setValue(30)  # Valor predeterminado: 30
        time_value_layout.addWidget(self.time_value_spin)
        
        # Unidad de tiempo
        self.time_unit_combo = QComboBox()
        self.time_unit_combo.addItems([
            self.i18n.get_text("seconds"),
            self.i18n.get_text("minutes"),
            self.i18n.get_text("hours")
        ])
        self.time_unit_combo.setCurrentIndex(1)  # Predeterminado: minutos
        time_value_layout.addWidget(self.time_unit_combo)
        
        time_form.addRow(self.i18n.get_text("time_value"), time_value_layout)
        time_layout.addWidget(time_group)
        
        # Pestaña de programación por hora exacta
        exact_time_tab = QWidget()
        exact_time_layout = QVBoxLayout(exact_time_tab)
        
        # Grupo de configuración de hora exacta
        exact_time_group = QGroupBox(self.i18n.get_text("tab_exact_time"))
        exact_time_form = QFormLayout(exact_time_group)
        
        # Selector de hora exacta
        self.exact_time_edit = QTimeEdit()
        self.exact_time_edit.setDisplayFormat("HH:mm")
        self.exact_time_edit.setTime(QTime.currentTime().addSecs(1800))  # +30 min
        exact_time_form.addRow(
            self.i18n.get_text("exact_time"), self.exact_time_edit
        )
        
        exact_time_layout.addWidget(exact_time_group)
        
        # Agregar pestañas al widget de pestañas
        self.tab_widget.addTab(time_tab, self.i18n.get_text("tab_time"))
        self.tab_widget.addTab(
            exact_time_tab, self.i18n.get_text("tab_exact_time")
        )
        
        # Grupo de selección de acción
        action_group = QGroupBox()
        action_layout = QHBoxLayout(action_group)
        
        # Radio buttons para seleccionar acción
        self.action_group = QButtonGroup(self)
        self.shutdown_radio = QRadioButton(self.i18n.get_text("action_shutdown"))
        self.restart_radio = QRadioButton(self.i18n.get_text("action_restart"))
        
        # Cargar iconos para los radio buttons
        shutdown_icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'icons', 'shutdown_icon.svg'
        )
        restart_icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'icons', 'restart_icon.svg'
        )
        
        self.shutdown_radio.setIcon(QIcon(shutdown_icon_path))
        self.restart_radio.setIcon(QIcon(restart_icon_path))
        
        self.action_group.addButton(self.shutdown_radio)
        self.action_group.addButton(self.restart_radio)
        self.shutdown_radio.setChecked(True)  # Predeterminado: apagado
        
        action_layout.addWidget(self.shutdown_radio)
        action_layout.addWidget(self.restart_radio)
        
        main_layout.addWidget(action_group)
        
        # Botón de programar
        self.schedule_button = QPushButton(self.i18n.get_text("schedule_button"))
        main_layout.addWidget(self.schedule_button)
        
        # Barra de progreso para la cuenta regresiva
        progress_layout = QHBoxLayout()
        progress_label = QLabel(self.i18n.get_text("remaining_time"))
        progress_layout.addWidget(progress_label)
        
        self.remaining_time_label = QLabel("--:--:--")
        self.remaining_time_label.setObjectName("remainingTimeLabel")
        progress_layout.addWidget(self.remaining_time_label)
        
        main_layout.addLayout(progress_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Botón de cancelar
        cancel_icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'icons', 'cancel_icon.svg'
        )
        
        self.cancel_button = QPushButton(self.i18n.get_text("cancel_button"))
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.setIcon(QIcon(cancel_icon_path))
        self.cancel_button.setEnabled(False)  # Inicialmente deshabilitado
        main_layout.addWidget(self.cancel_button)
        
        # Switch de tema claro/oscuro
        theme_layout = QHBoxLayout()
        
        theme_icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'icons', 'theme_icon.svg'
        )
        
        theme_label = QLabel()
        theme_label.setPixmap(QPixmap(theme_icon_path).scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        theme_layout.addWidget(theme_label)
        
        self.theme_switch = QCheckBox()
        self.theme_switch.setObjectName("themeSwitch")
        theme_layout.addWidget(self.theme_switch)
        
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

    def _setup_tray_icon(self):
        """Configura el icono de la bandeja del sistema."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setToolTip(self.i18n.get_text("tray_tooltip"))
        
        # Menú de la bandeja del sistema
        tray_menu = QMenu()
        
        show_action = QAction(self.i18n.get_text("tray_show"), self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        exit_action = QAction(self.i18n.get_text("tray_exit"), self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._tray_icon_activated)
        
        # Mostrar el icono en la bandeja
        self.tray_icon.show()

    def _setup_shortcuts(self):
        """Configura los atajos de teclado."""
        # Estos atajos se configurarán en el controlador
        pass

    def _tray_icon_activated(self, reason):
        """Maneja la activación del icono de la bandeja.

        Args:
            reason: Razón de la activación
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()

    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana.

        Args:
            event: Evento de cierre
        """
        # Si hay una acción programada, minimizar a la bandeja en lugar de cerrar
        if self.cancel_button.isEnabled() and self.controller.get_config('minimize_to_tray'):
            event.ignore()
            self.hide()
            return
        
        # Cerrar normalmente
        event.accept()

    def update_countdown(self):
        """Actualiza la cuenta regresiva en la interfaz."""
        # Esta función será implementada por el controlador
        pass

    def show_confirmation_dialog(self, action_type, time_str):
        """Muestra un diálogo de confirmación antes de programar una acción.

        Args:
            action_type (str): Tipo de acción ('shutdown' o 'restart')
            time_str (str): Tiempo formateado

        Returns:
            bool: True si el usuario confirma, False en caso contrario
        """
        action_text = self.i18n.get_text(f"action_{action_type}")
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.i18n.get_text("confirm_title"))
        msg_box.setText(
            self.i18n.get_text(
                "confirm_message",
                action=action_text.lower(),
                time=time_str
            )
        )
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        return msg_box.exec_() == QMessageBox.Yes

    def show_error_message(self, message):
        """Muestra un mensaje de error.

        Args:
            message (str): Mensaje de error
        """
        QMessageBox.critical(
            self,
            self.i18n.get_text("error"),
            message
        )

    def show_success_message(self, message):
        """Muestra un mensaje de éxito.

        Args:
            message (str): Mensaje de éxito
        """
        QMessageBox.information(
            self,
            self.i18n.get_text("success"),
            message
        )

    def show_admin_required_message(self):
        """Muestra un mensaje indicando que se requieren permisos de administrador."""
        QMessageBox.warning(
            self,
            self.i18n.get_text("admin_required"),
            self.i18n.get_text("admin_message")
        )

    def show_notification(self, title, message):
        """Muestra una notificación del sistema.

        Args:
            title (str): Título de la notificación
            message (str): Mensaje de la notificación
        """
        if self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)

    def apply_theme(self, theme):
        """Aplica un tema a la interfaz.

        Args:
            theme (str): 'light' o 'dark'
        """
        # Cargar el archivo de estilo correspondiente
        style_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'styles', f"{theme}.qss"
        )
        
        try:
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
            
            # Actualizar el estado del switch de tema
            self.theme_switch.setChecked(theme == 'dark')
        except Exception as e:
            print(f"Error al cargar el tema: {str(e)}")

    def get_current_action(self):
        """Obtiene la acción seleccionada actualmente.

        Returns:
            str: 'shutdown' o 'restart'
        """
        return 'shutdown' if self.shutdown_radio.isChecked() else 'restart'

    def get_time_value(self):
        """Obtiene el valor de tiempo ingresado.

        Returns:
            int: Valor de tiempo
        """
        return self.time_value_spin.value()

    def get_time_unit(self):
        """Obtiene la unidad de tiempo seleccionada.

        Returns:
            str: 'seconds', 'minutes' o 'hours'
        """
        index = self.time_unit_combo.currentIndex()
        units = ['seconds', 'minutes', 'hours']
        return units[index]

    def get_exact_time(self):
        """Obtiene la hora exacta seleccionada.

        Returns:
            str: Hora en formato HH:MM
        """
        return self.exact_time_edit.time().toString("HH:mm")

    def get_active_tab(self):
        """Obtiene el índice de la pestaña activa.

        Returns:
            int: Índice de la pestaña (0: tiempo, 1: hora exacta)
        """
        return self.tab_widget.currentIndex()

    def set_progress(self, value, max_value):
        """Establece el valor de la barra de progreso.

        Args:
            value (int): Valor actual
            max_value (int): Valor máximo
        """
        if max_value > 0:
            percentage = int((value / max_value) * 100)
            self.progress_bar.setValue(percentage)
        else:
            self.progress_bar.setValue(0)

    def set_remaining_time(self, time_str):
        """Establece el texto del tiempo restante.

        Args:
            time_str (str): Tiempo formateado (HH:MM:SS)
        """
        self.remaining_time_label.setText(time_str)

    def set_cancel_button_enabled(self, enabled):
        """Habilita o deshabilita el botón de cancelar.

        Args:
            enabled (bool): True para habilitar, False para deshabilitar
        """
        self.cancel_button.setEnabled(enabled)

    def set_schedule_button_enabled(self, enabled):
        """Habilita o deshabilita el botón de programar.

        Args:
            enabled (bool): True para habilitar, False para deshabilitar
        """
        self.schedule_button.setEnabled(enabled)