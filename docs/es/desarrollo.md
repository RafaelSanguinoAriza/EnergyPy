# EnergyPy — Desarrollo

Configuración del entorno de desarrollo, compilación y contribución.

---

## Requisitos

| Herramienta | Versión mínima | Verificar |
|---|---|---|
| Node.js | 20+ | `node --version` |
| npm | 9+ | `npm --version` |
| Rust | 1.77+ (stable) | `rustc --version` |
| Cargo | Latest | `cargo --version` |

### Dependencias del sistema

**Windows:**
- Visual Studio Build Tools 2022 (componente "Trabajo de desarrollo de C++")
- WebView2 Runtime (incluido en Windows 10/11 actualizado)

**Linux (Ubuntu/Debian):**
```bash
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget \
  file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

**Linux (Fedora):**
```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install webkit2gtk4.1-devel openssl-devel curl wget file \
  libappindicator-gtk3-devel librsvg2-devel
```

**macOS:**
```bash
xcode-select --install
```

---

## Inicio rápido

```bash
git clone https://github.com/RafaelSanguinoAriza/EnergyPy.git
cd EnergyPy
npm install
npm run tauri dev
```

---

## Scripts disponibles

| Comando | Descripción |
|---|---|
| `npm install` | Instalar dependencias del frontend |
| `npm run check` | Verificación de tipos TypeScript + Svelte |
| `npm run check:watch` | Verificación en modo watch |
| `npm test` | Ejecutar tests unitarios del frontend (Vitest) |
| `npm run test:ui` | Interfaz web de Vitest |
| `npm run tauri dev` | Servidor de desarrollo con recarga en caliente |
| `npm run tauri build` | Compilar versiones de producción |
| `cargo test` | Ejecutar tests del backend (en `src-tauri/`) |

---

## Estructura del proyecto

```
EnergyPy_V2.0/
├── src/                          # Frontend SvelteKit
│   ├── routes/                   # Páginas (routing basado en archivos)
│   │   ├── +layout.svelte        # Layout global: sidebar, header, transiciones, toast
│   │   ├── +layout.server.ts     # Server load: language from system settings
│   │   ├── +page.server.ts       # Redirect: / → /dashboard
│   │   ├── dashboard/
│   │   │   └── +page.svelte      # Bento grid: CPU, Memory, Disk, Network, SystemInfo, HealthBar, ProcessList
│   │   ├── processes/
│   │   │   └── +page.svelte      # Process manager: table with search, sort, kill
│   │   ├── power/
│   │   │   └── +page.svelte      # Power control: scheduling + manual execution
│   │   └── settings/
│   │       └── +page.svelte      # Settings: language, theme, notifications, autostart, refresh rate, about
│   ├── lib/
│   │   ├── components/
│   │   │   ├── dashboard/        # Dashboard components
│   │   │   │   ├── CpuCard.svelte
│   │   │   │   ├── MemoryCard.svelte
│   │   │   │   ├── DiskCard.svelte
│   │   │   │   ├── NetworkCard.svelte
│   │   │   │   ├── SystemInfoCard.svelte
│   │   │   │   ├── SystemHealthBar.svelte
│   │   │   │   └── ProcessList.svelte
│   │   │   ├── processes/
│   │   │   │   └── ProcessTable.svelte
│   │   │   ├── power/
│   │   │   │   └── ActionForm.svelte
│   │   │   └── ui/               # Componentes reutilizables
│   │   │       ├── Button.svelte
│   │   │       ├── Card.svelte
│   │   │       ├── Input.svelte
│   │   │       ├── Select.svelte
│   │   │       ├── Slider.svelte
│   │   │       ├── Badge.svelte
│   │   │       ├── Tooltip.svelte
│   │   │       ├── Sidebar.svelte
│   │   │       ├── Header.svelte
│   │   │       ├── Progress.svelte
│   │   │       ├── Skeleton.svelte
│   │   │       ├── SkeletonCard.svelte
│   │   │       ├── Toast.svelte
│   │   │       ├── SystemLogo.svelte
│   │   │       ├── SystemLogoFavicon.svelte
│   │   │       └── EnergyPyLogo.svelte
│   │   ├── i18n/                 # Internacionalización
│   │   │   ├── en.json
│   │   │   └── es.json
│   │   ├── stores/               # Estado global (Svelte 5 runes)
│   │   │   ├── config.ts         # AppConfig — language, theme, notifications, start_minimized, tray_enabled, auto_start, refresh_rate
│   │   │   ├── language.ts       # Current language + translations
│   │   │   ├── system.ts         # System data: CpuInfo, MemoryInfo, DiskInfo, NetworkInfo, BatteryInfo, ProcessInfo
│   │   │   ├── power.ts          # Power state: is_timer_running, timer_action, timer_total_seconds, timer_remaining_seconds
│   │   │   └── toast.ts          # Toast notifications: success, error, warning, info
│   │   ├── tauri.ts              # Wrapper functions for Tauri IPC invoke
│   │   └── constants.ts          # Route constants
│   └── app.html                  # HTML shell
├── src-tauri/                    # Backend Rust (Tauri)
│   ├── Cargo.toml                # Rust dependencies + metadata (v2.0.1)
│   ├── tauri.conf.json           # Tauri configuration (v2.0.1)
│   ├── src/
│   │   ├── lib.rs                # Tauri setup + IPC commands + app setup + COM STA init (Windows)
│   │   ├── system_monitor.rs     # sysinfo: CPU (with temperature via Components), Memory, Disk, Network, Battery, Processes
│   │   ├── power_manager.rs      # Power actions: shutdown, restart, suspend, hibernate, lock (cross-platform)
│   │   └── config.rs             # AppConfig persistence (JSON file in app config dir)
│   └── icons/                    # App icons
├── tests/                        # Tests unitarios
│   └── formatters.test.ts        # Tests de formateo de datos del sistema
├── docs/                         # Documentación profesional
│   ├── en/                       # English documentation
│   │   ├── README.md
│   │   ├── installation.md
│   │   ├── usage.md
│   │   ├── development.md
│   │   ├── architecture.md
│   │   └── configuration.md
│   └── es/                       # Documentación en español
│       ├── README.md
│       ├── instalacion.md
│       ├── uso.md
│       ├── desarrollo.md
│       ├── arquitectura.md
│       └── configuracion.md
├── README.md                     # Main README
├── CHANGELOG.md                  # Changelog (v2.0.1)
├── LICENSE                       # MIT License
└── package.json                  # npm scripts + dependencies
```

---

## Debugging

### Frontend (SvelteKit)

- El servidor de desarrollo se ejecuta en `http://localhost:5173/`.
- Usa las DevTools del navegador para inspeccionar el frontend.
- Los logs de Tauri se muestran en la terminal donde ejecutas `npm run tauri dev`.

### Backend (Rust)

- Los logs se escriben en `logs/energy_py.log` (modo desarrollo) o en el directorio de configuración (modo producción).
- Nivel de log: `Debug` en desarrollo, `Info` en producción.
- Usa `RUST_LOG=debug npm run tauri dev` para logs detallados.

### Tests

```bash
# Frontend
npm test

# Backend (desde src-tauri/)
cargo test
```

---

## Compilación para producción

```bash
npm run tauri build
```

Los instaladores quedan en `src-tauri/target/release/bundle/`:
- **Windows:** `nsis/` (instalador NSIS) o `msi/` (instalador MSI)
- **Linux:** `deb/` (paquete Debian) o `appimage/` (AppImage)
- **macOS:** `dmg/` (imagen de disco)

### Zip portátil (Windows)

Tras compilar con `npm run tauri build`:

```powershell
New-Item -ItemType Directory -Path dist\EnergyPy -Force
Copy-Item src-tauri\target\release\energypy_v20.exe, src-tauri\target\release\WebView2Loader.dll dist\EnergyPy\
Compress-Archive -Path dist\EnergyPy -DestinationPath dist\EnergyPy_2.0.1_x64_portable.zip
Remove-Item dist\EnergyPy -Recurse -Force
```

---

## Convenciones de código

- **Componentes:** PascalCase (`CpuCard.svelte`)
- **Stores:** camelCase (`system.ts` → `systemStore`)
- **Funciones IPC:** snake_case en Rust (`get_system_stats`), camelCase en TypeScript (`getSystemStats`)
- **Estilos:** Tailwind CSS con theme personalizado
- **Tests:** Vitest con describe/it blocks en inglés

---

## Changelog

Consulta [CHANGELOG.md](../../CHANGELOG.md) para ver los cambios recientes.
