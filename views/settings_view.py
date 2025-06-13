"""
Vista de configuración de la aplicación EnergyPy.

Este módulo implementa la interfaz gráfica para la configuración
de la aplicación, permitiendo al usuario personalizar sus preferencias.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QComboBox, QGroupBox, QFormLayout, QTabWidget,
    QWidget, QDialogButtonBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon


class SettingsView(QDialog):
    """Vista de configuración de la aplicación."""
    
    # Señal que se emite cuando se cambian las configuraciones
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent, i18n, config_model):
        """Inicializa la vista de configuración.

        Args:
            parent: Widget padre
            i18n: Instancia de internacionalización
            config_model: Modelo de configuración
        """
        super().__init__(parent)
        self.i18n = i18n
        self.config_model = config_model
        self._init_ui()

    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Configuración de la ventana
        self.setWindowTitle(self.i18n.get_text("settings"))
        self.setMinimumSize(400, 300)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Pestañas de configuración
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Pestaña de configuración general
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Grupo de idioma
        language_group = QGroupBox(self.i18n.get_text("language"))
        language_layout = QVBoxLayout(language_group)
        
        self.language_combo = QComboBox()
        # Agregar idiomas disponibles
        for lang_code in self.i18n.get_available_languages():
            self.language_combo.addItem(
                self.i18n.get_language_name(lang_code), lang_code
            )
        
        # Seleccionar el idioma actual
        current_lang = self.config_model.get_language()
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
        
        language_layout.addWidget(self.language_combo)
        general_layout.addWidget(language_group)
        
        # Grupo de notificaciones
        notifications_group = QGroupBox(self.i18n.get_text("notifications"))
        notifications_layout = QVBoxLayout(notifications_group)
        
        self.show_notifications_check = QCheckBox(
            self.i18n.get_text("notifications")
        )
        self.show_notifications_check.setChecked(
            self.config_model.get_config("show_notifications")
        )
        notifications_layout.addWidget(self.show_notifications_check)
        
        general_layout.addWidget(notifications_group)
        
        # Grupo de comportamiento
        behavior_group = QGroupBox("Comportamiento")
        behavior_layout = QVBoxLayout(behavior_group)
        
        self.minimize_to_tray_check = QCheckBox(
            self.i18n.get_text("minimize_to_tray")
        )
        self.minimize_to_tray_check.setChecked(
            self.config_model.get_config("minimize_to_tray")
        )
        behavior_layout.addWidget(self.minimize_to_tray_check)
        
        self.start_minimized_check = QCheckBox(
            self.i18n.get_text("start_minimized")
        )
        self.start_minimized_check.setChecked(
            self.config_model.get_config("start_minimized")
        )
        behavior_layout.addWidget(self.start_minimized_check)
        
        general_layout.addWidget(behavior_group)
        
        # Pestaña de atajos de teclado
        shortcuts_tab = QWidget()
        shortcuts_layout = QVBoxLayout(shortcuts_tab)
        
        shortcuts_group = QGroupBox(self.i18n.get_text("keyboard_shortcuts"))
        shortcuts_form = QFormLayout(shortcuts_group)
        
        # Mostrar los atajos actuales (solo lectura por ahora)
        keyboard_shortcuts = self.config_model.get_config("keyboard_shortcuts")
        
        for action, shortcut in keyboard_shortcuts.items():
            action_label = QLabel(action.capitalize())
            shortcut_label = QLabel(shortcut)
            shortcuts_form.addRow(action_label, shortcut_label)
        
        shortcuts_layout.addWidget(shortcuts_group)
        
        # Agregar pestañas al widget de pestañas
        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(shortcuts_tab, self.i18n.get_text("keyboard_shortcuts"))
        
        # Botones de acción
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel | QDialogButtonBox.Reset
        )
        
        # Traducir los botones
        button_box.button(QDialogButtonBox.Save).setText(
            self.i18n.get_text("save")
        )
        button_box.button(QDialogButtonBox.Cancel).setText(
            self.i18n.get_text("cancel_button")
        )
        button_box.button(QDialogButtonBox.Reset).setText(
            self.i18n.get_text("reset")
        )
        
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_settings
        )
        
        main_layout.addWidget(button_box)

    def _on_accept(self):
        """Maneja el evento de aceptar los cambios."""
        # Obtener la configuración actualizada
        new_settings = self.get_settings()
        
        # Emitir la señal con la nueva configuración
        self.settings_changed.emit(new_settings)
        
        # Usar QTimer para retrasar la llamada a accept() y evitar problemas con el objeto C/C++
        QTimer.singleShot(100, self.accept)

    def get_settings(self):
        """Obtiene la configuración seleccionada por el usuario.

        Returns:
            dict: Configuración seleccionada
        """
        # Obtener el código de idioma seleccionado
        lang_index = self.language_combo.currentIndex()
        language = self.language_combo.itemData(lang_index)
        
        return {
            "language": language,
            "show_notifications": self.show_notifications_check.isChecked(),
            "minimize_to_tray": self.minimize_to_tray_check.isChecked(),
            "start_minimized": self.start_minimized_check.isChecked()
        }

    def reset_settings(self):
        """Restablece la configuración a los valores predeterminados."""
        # Restablecer idioma
        default_lang = self.config_model.default_config["language"]
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == default_lang:
                self.language_combo.setCurrentIndex(i)
                break
        
        # Restablecer otras opciones
        self.show_notifications_check.setChecked(
            self.config_model.default_config["show_notifications"]
        )
        self.minimize_to_tray_check.setChecked(
            self.config_model.default_config["minimize_to_tray"]
        )
        self.start_minimized_check.setChecked(
            self.config_model.default_config["start_minimized"]
        )