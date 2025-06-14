"""
Vista de acerca de la aplicación EnergyPy.

Este módulo implementa la interfaz gráfica para mostrar información
sobre la aplicación, versión, autor, etc.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon


class AboutView(QDialog):
    """Vista de acerca de la aplicación."""

    def __init__(self, parent, i18n):
        """
        Inicializa la vista de acerca de.

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
        self.setFixedSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Logo de la aplicación
        logo_label = QLabel()
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'resources', 'icons', 'app_icon.svg'
        )
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(logo_label)
        
        # Título de la aplicación
        title_label = QLabel("EnergyPy")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Versión
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)
        
        # Descripción
        description_label = QLabel(self.i18n.get_text("about_description"))
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(description_label)
        
        # Autor
        author_label = QLabel("© 2025 - RafaelSanguino")
        author_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(author_label)
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.button(QDialogButtonBox.Ok).setText(self.i18n.get_text("ok"))
        
        main_layout.addWidget(button_box)