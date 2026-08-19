# EnergyPy — Instalación

Guía de instalación para Windows, Linux y macOS.

---

## Requisitos previos

| Componente | Windows | Linux | macOS |
|---|---|---|---|
| Sistema operativo | Windows 10/11 (64-bit) | Ubuntu 22.04+ / Fedora 38+ | macOS 13 Ventura+ |
| Runtime | WebView2 (incluido en Win 10/11 actualizado) | libwebkit2gtk | WebKit (incluido en macOS) |
| RAM | 256 MB libres | 256 MB libres | 256 MB libres |
| Disco | ~22 MB | ~22 MB | ~22 MB |

---

## Windows

### Instalador NSIS (recomendado)

1. Descarga `EnergyPy_2.0.1_x64-setup.exe` desde [GitHub Releases](https://github.com/RafaelSanguinoAriza/EnergyPy/releases).
2. Ejecuta el instalador. No requiere permisos de administrador.
3. La app se instala en `C:\Users\<tu_usuario>\AppData\Local\EnergyPy\`.

### Instalador MSI

1. Descarga `EnergyPy_2.0.1_x64_en-US.msi` desde [GitHub Releases](https://github.com/RafaelSanguinoAriza/EnergyPy/releases).
2. Ejecuta el MSI. Puede requerir permisos de administrador según tu configuración.

### Versión portátil

1. Descarga `EnergyPy_2.0.1_x64_portable.zip`.
2. Extrae el zip a cualquier carpeta.
3. Ejecuta `energypy_v20.exe` directamente.
4. **Importante:** `WebView2Loader.dll` debe permanecer junto al `.exe`.

> Si Windows SmartScreen muestra un aviso, haz clic en "Más información" y luego "Ejecutar de todas formas".

---

## Linux

> **Estado:** Próximamente. Las builds de Linux estarán disponibles cuando se complete la implementación del daemon D-Bus para el control de energía.

### Requisitos (próximamente)

```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev

# Fedora
sudo dnf install webkit2gtk4.1-devel libappindicator-gtk3-devel librsvg2-devel
```

---

## macOS

> **Estado:** Próximamente. Las builds de macOS estarán disponibles tras validar la integración con `pmset` y `launchd`.

### Requisitos (próximamente)

```bash
# Homebrew
brew install curl wget
```

---

## Verificación de la instalación

1. Abre EnergyPy desde el menú de inicio, el lanzador o la terminal.
2. Navega por las pestañas: Dashboard, Procesos, Energía, Configuración.
3. Verifica que los datos del sistema se actualizan correctamente.

---

## Solución de problemas

| Problema | Solución |
|---|---|
| EnergyPy no inicia en Windows | Verifica que WebView2 esté instalado: [descarga WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) |
| Pantalla blanca al iniciar | Actualiza los controladores de gráficos |
| Alta CPU en Linux | Verifica que el daemon de energía esté disponible |
| No se muestra la temperatura de CPU | Algunos sensores requieren permisos root en Linux |

---

## Siguiente paso

- [Uso de la aplicación](uso.md) — Guía completa de cada función.
