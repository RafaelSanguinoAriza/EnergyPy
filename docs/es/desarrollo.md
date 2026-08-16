# 💻 Guía de Desarrollo — EnergyPy

> **Índice de docs:** [README](../README.md) · [Instalación](instalacion.md) · [Uso](uso.md) · [Arquitectura](arquitectura.md) · [Configuración](configuracion.md)

---

## Prerrequisitos

| Herramienta | Versión mínima | Notas |
|---|---|---|
| [Node.js](https://nodejs.org) | 20+ | Incluye npm |
| [Rust](https://www.rust-lang.org/tools/install) | 1.77+ | Instala vía `rustup` |

### Dependencias por sistema operativo

**Windows**
- Opción A (recomendada): [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) con la carga de trabajo *"Desktop development with C++"*.
- Opción B: MSYS2 + MinGW-w64 (toolchain GNU), como se usa en este proyecto:
  ```
  rustup default stable-x86_64-pc-windows-gnu
  ```
  y asegúrate de que `C:\msys64\mingw64\bin` esté en el `PATH`.

> ⚠️ **Nota (Windows GNU):** este repositorio viene preparado para la
> toolchain GNU. El enlazador de MinGW (`ld`) desborda la tabla de exportación
> PE (error *"export ordinal too large"*) al compilar la `cdylib` de Tauri en
> debug; por eso `[profile.dev] opt-level = 2` está configurado en
> `src-tauri/Cargo.toml`. No elimines ese ajuste si compilas con GNU.

**Linux (Debian/Ubuntu)**
```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev \
  build-essential \
  curl \
  wget \
  file \
  libxdo-dev \
  libssl-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev
```

**macOS**
```bash
xcode-select --install
brew install webkit2gtk  # si es necesario
```

---

## Configuración del proyecto

```bash
# Clonar el repositorio
git clone <tu-repo>/EnergyPy.git
cd EnergyPy

# Instalar dependencias
npm install
```

---

## Scripts disponibles

| Comando | Descripción |
|---|---|
| `npm run dev` | Servidor de desarrollo Vite (solo frontend) |
| `npm run tauri dev` | Desarrollo completo: frontend + ventana nativa con recarga en caliente |
| `npm run build` | Compilación del frontend de producción |
| `npm run check` | Verificación de tipos (svelte-check + TypeScript) |
| `npm test` | Tests unitarios del frontend (Vitest) |
| `cargo test` | Tests del backend Rust (ejecutar en `src-tauri/`) |
| `npm run tauri build` | Compilación de instaladores de producción |
| `npm run tauri icon` | Regenera los iconos de la app desde un PNG fuente |

---

## Testing

```bash
npm test                 # Frontend: Vitest (tests/formatters.test.ts)
cargo test               # Backend: ejecutar dentro de src-tauri/
```

- Frontend: cubre las utilidades de formato (`formatBytes`, `formatUptime`,
  `formatTimeRemaining`, `formatDurationShort`, etc.).
- Backend: cubre la lógica de programación (`seconds_until`), la serialización
  de `ActionType` en lowercase y la detección de admin en `power_manager.rs`.

---

## Estructura del proyecto

```
EnergyPy/
├── src/                          # Frontend SvelteKit
│   ├── app.css                   # Tailwind CSS v4 + tema personalizado
│   ├── app.html                  # Plantilla HTML
│   ├── lib/
│   │   ├── components/
│   │   │   ├── dashboard/        # Tarjetas de monitoreo
│   │   │   ├── power/            # Formulario + countdown
│   │   │   ├── sidebar/          # Navegación
│   │   │   ├── theme/            # Selector de tema
│   │   │   └── ui/               # Componentes base (Card, Button, etc.)
│   │   ├── i18n/                 # Traducciones (en.json, es.json)
│   │   ├── stores/               # Stores de Svelte
│   │   ├── formatters.ts         # Utilidades de formato
│   │   ├── tauri.ts              # Wrappers de comandos Tauri
│   │   └── update.ts             # Utilidad de actualización
│   └── routes/                   # Páginas (dashboard, power, settings)
├── src-tauri/                    # Backend Rust
│   ├── src/
│   │   ├── lib.rs                # Entry point, estado, bandeja, threads
│   │   ├── system_monitor.rs     # Monitoreo de sistema (sysinfo)
│   │   ├── power_manager.rs      # Programación de acciones de energía
│   │   └── config.rs             # Persistencia de configuración
│   ├── icons/                    # Iconos generados
│   ├── capabilities/             # Permisos de la app
│   ├── Cargo.toml                # Dependencias Rust
│   └── tauri.conf.json           # Configuración de Tauri
├── docs/                         # Documentación (es/en)
├── static/                       # Assets estáticos
├── package.json
└── README.md
```

---

## Flujo de trabajo típico

1. **Modifica el frontend** en `src/` — los cambios se reflejan al instante con `tauri dev`.
2. **Modifica el backend** en `src-tauri/src/` — Tauri recompila el binario automáticamente.
3. **Añade un comando nuevo**:
   - En Rust: `#[tauri::command] fn mi_comando() { ... }` y agrégalo al `invoke_handler` en `lib.rs`.
   - En TS: añade un wrapper en `src/lib/tauri.ts` usando `invoke("mi_comando", args)`.
   - **Nota:** Tauri v2 convierte `snake_case` a `camelCase` en los argumentos (ej. `action_type` → `actionType`).
4. **Verifica tipos:** `npm run check`.
5. **Compila:** `npm run tauri build`.

---

## Agregar un idioma nuevo

1. Crea `src/lib/i18n/xx.json` con las mismas claves que `en.json`.
2. En `src/lib/i18n/index.ts`:
   - Importa el archivo: `import xx from "./xx.json";`
   - Añádelo al `Record`: `const translations = { en, es, xx };`
   - Añade el idioma a `availableLanguages`.
3. Agrega la traducción de todos los textos de la app.

---

## Sistema de logging

La app usa `log` + `simplelog`. Los logs se escriben a un archivo:
- **Windows**: `%APPDATA%\EnergyPy\energypy.log`
- **Linux**: `~/.config/EnergyPy/energypy.log`
- **macOS**: `~/Library/Application Support/EnergyPy/energypy.log`

Para añadir logging en Rust:
```rust
log::info!("mensaje");
log::warn!("advertencia");
log::error!("error");
```

---

## Compilación de producción

```bash
npm run tauri build
```

### Salidas (Windows)

| Formato | Ruta |
|---|---|
| Ejecutable | `src-tauri/target/release/energypy_v20.exe` |
| MSI | `src-tauri/target/release/bundle/msi/EnergyPy_2.0.0_x64_en-US.msi` |
| NSIS | `src-tauri/target/release/bundle/nsis/EnergyPy_2.0.0_x64-setup.exe` |

### Regenerar iconos

```bash
npm run tauri icon <archivo-png-1024x1024>
```

---

## Publicación y seguridad

Antes de publicar el repositorio o un release:

1. Sustituye `YOUR_GITHUB_USER` por el usuario real (`RafaelSanguinoAriza`) en
   `src-tauri/tauri.conf.json` (campo `plugins.updater.endpoints`).
2. Configura los secretos de GitHub `TAURI_SIGNING_PRIVATE_KEY` y
   `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` (ver `.github/workflows/release.yml`).
3. Revisa [SECURITY.md](../../SECURITY.md) — el archivo `.updater-key`
   (clave privada) no debe publicarse jamás y ya está excluido en `.gitignore`.

---

[← Uso](uso.md) · [Siguiente: Arquitectura →](arquitectura.md)