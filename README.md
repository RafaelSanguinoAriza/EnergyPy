<div align="center">

# ⚡ EnergyPy

**Monitor de sistema y control de energía de escritorio multiplataforma**

[![Tauri v2](https://img.shields.io/badge/Tauri-v2-24C8DB)](https://v2.tauri.app)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-5-FF3E00)](https://svelte.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)](https://www.typescriptlang.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-orange)](https://www.rust-lang.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

EnergyPy es una aplicación de escritorio que monitorea el sistema en tiempo real y permite programar acciones de energía (apagado, reinicio, suspensión, hibernación y bloqueo) con una interfaz moderna y ligera.

> **English readers:** the [English documentation](docs/en/) is available in the `docs/en/` folder.

---

## ✨ Características

- 📊 **Dashboard en vivo** — Uso de CPU (por núcleo), memoria, disco, red, tiempo de actividad y batería, actualizado cada 2 segundos.
- ⏰ **Programación de energía** — Agenda apagado, reinicio, suspensión, hibernación o bloqueo con temporizador y barra de progreso.
- 🌍 **Multilenguaje** — Interfaz completa en español e inglés con cambio instantáneo.
- 🌙 **Temas** — Tema claro, oscuro o seguir al sistema.
- 🗔 **Bandeja del sistema** — Minimiza a la bandeja para operar en segundo plano.
- ⌨️ **Atajos de teclado** — `Ctrl+C` (cancelar), `Ctrl+T` (tema), `Ctrl+Q` (salir).
- 🔄 **Actualización automática** — Mecanismo integrado vía GitHub Releases.

---

## 📥 Descarga

Descarga la última versión desde **[GitHub Releases](https://github.com/RafaelSanguinoAriza/EnergyPy/releases)**. Elige tu sistema operativo y pulsa sobre la opción que quieras: cada botón corresponde al archivo que debes descargar.

### 🪟 Windows

[![Windows - Instalador NSIS (recomendado)](https://img.shields.io/badge/Windows-Instalador_NSIS_%28recomendado%29-0078D6?style=for-the-badge)](https://github.com/RafaelSanguinoAriza/EnergyPy/releases/download/EnergyPy/EnergyPy_2.0.0_x64-setup.exe)
[![Windows - Instalador MSI](https://img.shields.io/badge/Windows-Instalador_MSI-0078D6?style=for-the-badge)](https://github.com/RafaelSanguinoAriza/EnergyPy/releases/download/EnergyPy/EnergyPy_2.0.0_x64_en-US.msi)
[![Windows - Versión portátil (.zip)](https://img.shields.io/badge/Windows-Versi%C3%B3n_port%C3%A1til_%28.zip%29-0078D6?style=for-the-badge)](https://github.com/RafaelSanguinoAriza/EnergyPy/releases/download/EnergyPy/EenergyPy_v2.0.0.zip)

### 🐧 Linux

![Linux - Próximamente](https://img.shields.io/badge/Linux-Pr%C3%B3ximamente-FCC624?style=for-the-badge&logo=linux&logoColor=black)

### 🍎 macOS

![macOS - Próximamente](https://img.shields.io/badge/macOS-Pr%C3%B3ximamente-333333?style=for-the-badge&logo=apple&logoColor=white)

> 💡 **¿Cuál descargo?** — Si usas **Windows**, elige **Instalador NSIS** (se instala sin permisos de administrador) o **Versión portátil** si no quieres instalar nada. Las versiones de **Linux** y **macOS** estarán disponibles próximamente.

### 🧳 Versión portátil (Windows)

El zip contiene una carpeta `EnergyPy/` con:
- `energypy_v20.exe` — la aplicación (interfaz y configuración embebidas en el binario).
- `WebView2Loader.dll` — cargador de Tauri; **debe permanecer junto al `.exe`**.
- `LEEME.txt` — instrucciones y requisitos.

**Requisitos**: Windows 10/11 de 64 bits con el runtime Microsoft Edge WebView2 (viene preinstalado en sistemas actualizados). No requiere instalación: extrae la carpeta y ejecuta `energypy_v20.exe`.

> ⚠️ Al no estar firmado digitalmente, Windows SmartScreen puede mostrar un aviso en la primera ejecución (tanto en el instalador como en la versión portátil).

---

## 🚀 Uso rápido

| Sección | Descripción |
|---|---|
| **Dashboard** | Monitoreo en tiempo real de todos los recursos del sistema |
| **Control de Energía** | Programa acciones de energía con temporizador o a hora exacta |
| **Configuración** | Idioma, tema, notificaciones y atajos de teclado |

---

## 📖 Documentación completa

Consulta la documentación detallada y profesional en:

| Idioma | Enlace |
|---|---|
| 🇪🇸 **Español** | [docs/es/](docs/es/) |
| 🇬🇧 **English** | [docs/en/](docs/en/) |

### Guías en español
- [Instalación](docs/es/instalacion.md) — Requisitos e instalación por sistema operativo
- [Uso](docs/es/uso.md) — Guía detallada de todas las funciones
- [Desarrollo](docs/es/desarrollo.md) — Configuración del entorno y compilación
- [Arquitectura](docs/es/arquitectura.md) — Diseño interno de la aplicación
- [Configuración](docs/es/configuracion.md) — Referencia de opciones de configuración

---

## 🛠️ Desarrollo

```bash
# Prerrequisitos: Node.js 20+, Rust stable, dependencias del sistema

npm install              # Instalar dependencias
npm run tauri dev        # Servidor de desarrollo con recarga en caliente
npm run check            # Verificación de tipos TypeScript + Svelte
npm test                 # Tests unitarios del frontend (Vitest)
npm run tauri build      # Compilar instaladores de producción
```

Los instaladores (NSIS/MSI) quedan en `src-tauri/target/release/bundle/`. Para
generar el **zip portátil** tras el build (exe + `WebView2Loader.dll` + `LEEME.txt`):

```powershell
New-Item -ItemType Directory -Path dist\EnergyPy -Force
Copy-Item src-tauri\target\release\energypy_v20.exe, src-tauri\target\release\WebView2Loader.dll dist\EnergyPy\
Compress-Archive -Path dist\EnergyPy -DestinationPath dist\EnergyPy_2.0.0_x64_portable.zip
Remove-Item dist\EnergyPy -Recurse -Force
```

> 📌 En Windows con toolchain GNU, asegúrate de que `C:\msys64\mingw64\bin`
> esté en el `PATH`. Ver [desarrollo](docs/es/desarrollo.md).

---

## 🧪 Testing

| Suite | Comando | Ubicación |
|---|---|---|
| Frontend (Vitest) | `npm test` | `tests/formatters.test.ts` |
| Backend (cargo) | `cargo test` (en `src-tauri/`) | tests en `power_manager.rs` |

---

## 🗂️ Stack tecnológico

| Capa | Tecnología |
|---|---|
| Shell de escritorio | [Tauri v2](https://v2.tauri.app) |
| Frontend | [SvelteKit 5](https://svelte.dev) + [TypeScript](https://www.typescriptlang.org) |
| Estilos | [Tailwind CSS v4](https://tailwindcss.com) |
| Iconos | [Lucide](https://lucide.dev) |
| Backend | [Rust](https://www.rust-lang.org) con [sysinfo](https://github.com/GuillaumeGomez/sysinfo) |
| Logging | `log` + `simplelog` |

---

## 📄 Licencia

[MIT](LICENSE)

---

## Changelog

Consulta [CHANGELOG.md](CHANGELOG.md) para el historial de cambios.
