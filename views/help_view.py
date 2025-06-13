"""
Vistas de ayuda y acerca de para la aplicación EnergyPy.

Este módulo implementa las interfaces gráficas para mostrar
información de ayuda y acerca de la aplicación.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextBrowser, QDialogButtonBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap


class HelpView(QDialog):
    """Vista de ayuda de la aplicación."""

    def __init__(self, parent, i18n):
        """Inicializa la vista de ayuda.

        Args:
            parent: Widget padre
            i18n: Instancia de internacionalización
        """
        super().__init__(parent)
        self.i18n = i18n
        self._init_ui()

    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Configuración de la ventana
        self.setWindowTitle(self.i18n.get_text("help"))
        self.setMinimumSize(500, 400)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Contenido de ayuda
        help_browser = QTextBrowser()
        help_browser.setOpenExternalLinks(True)
        help_browser.setHtml(self.i18n.get_text("help_content"))
        
        main_layout.addWidget(help_browser)
        
        # Botón de cerrar
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)


class AboutView(QDialog):
    """Vista de acerca de la aplicación."""

    def __init__(self, parent, i18n):
        """Inicializa la vista de acerca de.

        Args:
            parent: Widget padre
            i18n: Instancia de internacionalización
        """
        super().__init__(parent)
        self.i18n = i18n
        self._init_ui()

    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Configuración de la ventana
        self.setWindowTitle(self.i18n.get_text("about"))
        self.setMinimumSize(400, 300)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Icono de la aplicación
        icon_layout = QHBoxLayout()
        
        app_icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'icons', 'app_icon.svg'
        )
        
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(app_icon_path).scaled(
            64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        icon_layout.addStretch()
        icon_layout.addWidget(icon_label)
        icon_layout.addStretch()
        
        main_layout.addLayout(icon_layout)
        
        # Contenido de acerca de
        about_browser = QTextBrowser()
        about_browser.setOpenExternalLinks(True)
        about_browser.setHtml(self.i18n.get_text("about_content"))
        
        main_layout.addWidget(about_browser)
        
        # Botón de cerrar
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)