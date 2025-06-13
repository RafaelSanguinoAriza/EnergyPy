<div align="center">

# EnergyPy

<img src="resources/icons/app_icon.svg" alt="EnergyPy Logo" width="120" height="120">

**Una aplicación multiplataforma para programar el apagado o reinicio del sistema**

[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-blue.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt-5.15%2B-green)](https://pypi.org/project/PyQt5/)

</div>

## 📋 Índice

- [Descripción](#-descripción)
- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Descargas](#-descargas)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Personalización](#-personalización)
- [Compilación](#-compilación)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Desarrollador](#-desarrollador)

## 📝 Descripción

EnergyPy es una aplicación multiplataforma desarrollada en Python con PyQt5 que permite programar el apagado o reinicio del sistema de manera sencilla y eficiente. Diseñada para funcionar en Windows, macOS y Linux, ofrece una interfaz intuitiva y personalizable con soporte para múltiples idiomas y temas.

## ✨ Características

- **Programación por tiempo**: Establece un temporizador en segundos, minutos u horas
- **Programación por hora exacta**: Programa acciones para una hora específica del día
- **Acciones disponibles**: Apagado o reinicio del sistema
- **Interfaz moderna**: Diseño limpio e intuitivo con iconos vectoriales
- **Temas**: Modo claro y oscuro, con detección automática del tema del sistema
- **Multiidioma**: Soporte para español e inglés (extensible a más idiomas)
- **Bandeja del sistema**: Minimiza a la bandeja del sistema para un uso discreto
- **Atajos de teclado**: Acceso rápido a funciones comunes
- **Multiplataforma**: Compatible con Windows, macOS y Linux

## 🖼️ Capturas de Pantalla

<div align="center">
<p><i>Tema claro y oscuro disponibles</i></p>
</div>

## 💻 Requisitos del Sistema

- **Python**: 3.6 o superior
- **PyQt5**: 5.15.0 o superior
- **Sistemas Operativos**: Windows 7+, macOS 10.13+, o Linux con entorno de escritorio
- **Permisos**: Requiere permisos de administrador para ejecutar comandos de apagado/reinicio

## 🚀 Instalación

### Desde el código fuente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/RafaelSanguinoAriza/EnergyPy.git
   cd EnergyPy
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

### Desde el ejecutable

1. Descarga la última versión desde la sección de [Releases](https://github.com/RafaelSanguinoAriza/EnergyPy/releases)
2. Ejecuta `EnergyPy.exe` (Windows), `EnergyPy.app` (macOS) o `EnergyPy` (Linux) como administrador
3. Ya estás listo para usar EnergyPy!

## 📥 Descargas

<div align="center">

### Descarga EnergyPy para tu sistema operativo

<table>
  <tr>
    <td align="center">
      <a href="dist/EnergyPy-Windows.zip">
        <img src="resources/icons/windows.svg" alt="Windows" width="48" height="48"><br>
        <img src="https://img.shields.io/badge/DESCARGAR-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white">
      </a>
      <p>Windows 7 o superior</p>
    </td>
    <td align="center">
      <a href="#" style="pointer-events: none; cursor: default;">
        <img src="resources/icons/linux.svg" alt="Linux" width="48" height="48"><br>
        <img src="https://img.shields.io/badge/PRÓXIMAMENTE-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
      </a>
      <p>Próximamente</p>
    </td>
    <td align="center">
      <a href="#" style="pointer-events: none; cursor: default;">
        <img src="resources/icons/apple.svg" alt="macOS" width="48" height="48"><br>
        <img src="https://img.shields.io/badge/PRÓXIMAMENTE-macOS-000000?style=for-the-badge&logo=apple&logoColor=white">
      </a>
      <p>Próximamente</p>
    </td>
  </tr>
</table>

<p><i>Las versiones para Linux y macOS estarán disponibles próximamente. Mientras tanto, puedes ejecutar la aplicación desde el código fuente siguiendo las instrucciones de instalación.</i></p>

</div>

## 📖 Uso

### Programar por tiempo

1. Selecciona la pestaña "Programar por tiempo"
2. Ingresa el valor deseado y selecciona la unidad (segundos, minutos u horas)
3. Elige la acción (apagar o reiniciar)
4. Haz clic en "Programar"

### Programar por hora exacta

1. Selecciona la pestaña "Programar por hora"
2. Establece la hora exacta en formato HH:MM
3. Elige la acción (apagar o reiniciar)
4. Haz clic en "Programar"

### Cancelar una acción programada

- Haz clic en el botón "Cancelar"
- O utiliza el atajo de teclado Ctrl+C

### Atajos de teclado

- **Ctrl+C**: Cancelar acción programada
- **Ctrl+Tab**: Cambiar entre pestañas
- **Ctrl+T**: Cambiar tema (claro/oscuro)

## 📂 Estructura del Proyecto

```
EnergyPy/
├── controllers/           # Controladores (patrón MVC)
│   ├── __init__.py
│   └── main_controller.py # Controlador principal
├── models/                # Modelos de datos
│   ├── __init__.py
│   ├── config_model.py    # Gestión de configuración
│   └── system_model.py    # Operaciones del sistema
├── views/                 # Interfaces de usuario
│   ├── __init__.py
│   ├── about_view.py      # Vista de acerca de
│   ├── help_view.py       # Vista de ayuda
│   ├── main_view.py       # Vista principal
│   └── settings_view.py   # Vista de configuración
├── resources/             # Recursos estáticos
│   ├── icons/             # Iconos SVG
│   ├── styles/            # Hojas de estilo QSS
│   └── translations/      # Archivos de traducción
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── i18n.py            # Internacionalización
│   ├── logger.py          # Sistema de registro
│   └── paths.py           # Gestión de rutas
├── build.py               # Script de compilación
├── EnergyPy.spec          # Configuración de PyInstaller
├── LICENSE                # Licencia MIT
├── main.py                # Punto de entrada
└── requirements.txt       # Dependencias
```

## 🔧 Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **PyQt5**: Framework para la interfaz gráfica
- **PyInstaller**: Herramienta para crear ejecutables
- **JSON**: Almacenamiento de configuración y traducciones
- **SVG**: Iconos vectoriales escalables
- **QSS**: Hojas de estilo para personalización visual

## 🎨 Personalización

### Añadir un nuevo idioma

1. Crea un nuevo archivo JSON en `resources/translations/` (por ejemplo, `fr.json`)
2. Copia la estructura de `es.json` o `en.json` y traduce los valores
3. Añade el nuevo idioma en `models/config_model.py` en la lista de idiomas disponibles

### Modificar temas

Los archivos de tema se encuentran en `resources/styles/`:
- `light.qss`: Tema claro
- `dark.qss`: Tema oscuro

Puedes modificar estos archivos para personalizar la apariencia de la aplicación.

### Añadir nuevos iconos

1. Coloca los archivos SVG en `resources/icons/`
2. Utiliza la función `get_resource_path()` para cargarlos en la aplicación

## 🔨 Compilación

EnergyPy incluye un script de compilación que genera ejecutables para la plataforma actual:

```bash
python build.py
```

Esto generará un ejecutable en la carpeta `dist/` o `dist_new/` utilizando PyInstaller.

### Requisitos para compilación

- **Windows**: Icono en formato `.ico` en `resources/icon.ico`
- **macOS**: Icono en formato `.icns` en `resources/icon.icns`
- **Linux**: Icono en formato `.png` en `resources/icon.png`

## 👥 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`)
4. Sube los cambios a tu fork (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📜 Licencia

<div align="center">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="Licencia MIT"/>
  </a>
  <p>Este proyecto está licenciado bajo los términos de la <b>Licencia MIT</b>.</p>
</div>

### ¿Qué permite esta licencia?

- ✅ **Uso Comercial**: Puedes utilizar el software con fines comerciales.
- ✅ **Modificación**: Eres libre de modificar el código fuente para adaptarlo a tus necesidades.
- ✅ **Distribución**: Puedes redistribuir copias del software original o de tus versiones modificadas.
- ✅ **Uso Privado**: Puedes utilizar el software para fines personales y privados.
- ✅ **Sublicencia**: Puedes otorgar sublicencias del software bajo los términos de la Licencia MIT.

### Condiciones

- ℹ️ **Incluir Copyright y Licencia**: Debes incluir el aviso de copyright original y el texto completo de la Licencia MIT en todas las copias o partes sustanciales del software.
- ℹ️ **Sin Garantía**: El software se proporciona "tal cual", sin ninguna garantía expresa o implícita.
- ℹ️ **Sin Responsabilidad**: Los autores o titulares de los derechos de autor no serán responsables de ninguna reclamación, daño u otra responsabilidad que surja del uso del software.

---

## 👥 Desarrollador

<div align="center">
  <table>
    <tr>
      <td align="center" style="border: none; padding: 10px;">
        <a href="https://github.com/RafaelSanguinoAriza">
          <img src="https://github.com/RafaelSanguinoAriza.png" width="100px" style="border-radius: 50%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" alt="Rafael David Sanguino Ariza"/>
          <br />
          <sub><b>Rafael David Sanguino Ariza</b></sub>
        </a>
        <br />
        <sub style="font-size: 0.9em; color: #555;">💻 Desarrollador Full Stack</sub>
        <br><br>
        <a href="https://github.com/RafaelSanguinoAriza" style="margin-right: 5px;">
          <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
        </a>
        <a href="https://www.linkedin.com/in/rafael-david-sanguino-ariza/">
          <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
        </a>
      </td>
    </tr>
  </table>
</div>

---
<div align="center" style="padding-top: 20px; padding-bottom: 20px;">
  <h3 style="font-family: 'Poppins', sans-serif; font-weight: 700;">¡Gracias por tu interés en EnergyPy! 🔋</h3>
  <p style="font-size: 1em;">Espero disfrutes usando esta herramienta para programar el apagado o reinicio del sistema.</p>
  <p style="font-size: 0.9em;">Realizado con ❤️ en Bucaramanga 🇨🇴</p>
  <p style="margin-top: 15px;">¿Te gusta EnergyPy? ¡Dale una ⭐️ en GitHub!</p>
  
  <a href="https://github.com/RafaelSanguinoAriza/EnergyPY">
    <img src="https://img.shields.io/badge/Repositorio-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Repositorio"/>
  </a>
</div>

---
