# EnergyPy — Development

Development environment setup, building, and contributing.

---

## Requirements

| Tool | Minimum version | Verify |
|---|---|---|
| Node.js | 20+ | `node --version` |
| npm | 9+ | `npm --version` |
| Rust | 1.77+ (stable) | `rustc --version` |
| Cargo | Latest | `cargo --version` |

### System dependencies

**Windows:**
- Visual Studio Build Tools 2022 (C++ workload)
- WebView2 Runtime (included in updated Windows 10/11)

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

## Quick start

```bash
git clone https://github.com/RafaelSanguinoAriza/EnergyPy.git
cd EnergyPy
npm install
npm run tauri dev
```

---

## Available scripts

| Command | Description |
|---|---|
| `npm install` | Install frontend dependencies |
| `npm run check` | TypeScript + Svelte type checking |
| `npm run check:watch` | Type checking in watch mode |
| `npm test` | Run frontend unit tests (Vitest) |
| `npm run test:ui` | Vitest web interface |
| `npm run tauri dev` | Development server with hot reload |
| `npm run tauri build` | Build production versions |
| `cargo test` | Run backend tests (in `src-tauri/`) |

---

## Project structure

```
EnergyPy_V2.0/
├── src/                          # SvelteKit Frontend
│   ├── routes/                   # Pages (file-based routing)
│   │   ├── +layout.svelte        # Global layout: sidebar, header, transitions, toast
│   │   ├── +layout.server.ts     # Server load: language from system settings
│   │   ├── +page.server.ts       # Redirect: / → /dashboard
│   │   ├── dashboard/
│   │   │   └── +page.svelte      # Bento Grid: CPU, Memory, Disk, Network, SystemInfo, HealthBar, ProcessList
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
│   │   │   └── ui/               # Reusable components
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
│   │   ├── i18n/                 # Internationalization
│   │   │   ├── en.json
│   │   │   └── es.json
│   │   ├── stores/               # Global state (Svelte 5 runes)
│   │   │   ├── config.ts         # AppConfig — language, theme, notifications, start_minimized, tray_enabled, auto_start, refresh_rate
│   │   │   ├── language.ts       # Current language + translations
│   │   │   ├── system.ts         # System data: CpuInfo, MemoryInfo, DiskInfo, NetworkInfo, BatteryInfo, ProcessInfo
│   │   │   ├── power.ts          # Power state: is_timer_running, timer_action, timer_total_seconds, timer_remaining_seconds
│   │   │   └── toast.ts          # Toast notifications: success, error, warning, info
│   │   ├── tauri.ts              # Wrapper functions for Tauri IPC invoke
│   │   └── constants.ts          # Route constants
│   └── app.html                  # HTML shell
├── src-tauri/                    # Rust Backend (Tauri)
│   ├── Cargo.toml                # Rust dependencies + metadata (v2.0.1)
│   ├── tauri.conf.json           # Tauri configuration (v2.0.1)
│   ├── src/
│   │   ├── lib.rs                # Tauri setup + IPC commands + app setup + COM STA init (Windows)
│   │   ├── system_monitor.rs     # sysinfo: CPU (with temperature via Components), Memory, Disk, Network, Battery, Processes
│   │   ├── power_manager.rs      # Power actions: shutdown, restart, suspend, hibernate, lock (cross-platform)
│   │   └── config.rs             # AppConfig persistence (JSON file in app config dir)
│   └── icons/                    # App icons
├── tests/                        # Unit tests
│   └── formatters.test.ts        # System data formatting tests
├── docs/                         # Professional documentation
│   ├── en/                       # English documentation
│   │   ├── README.md
│   │   ├── installation.md
│   │   ├── usage.md
│   │   ├── development.md
│   │   ├── architecture.md
│   │   └── configuration.md
│   └── es/                       # Spanish documentation
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

- The development server runs at `http://localhost:5173/`.
- Use browser DevTools to inspect the frontend.
- Tauri logs are shown in the terminal where you run `npm run tauri dev`.

### Backend (Rust)

- Logs are written to `logs/energy_py.log` (development) or the config directory (production).
- Log level: `Debug` in development, `Info` in production.
- Use `RUST_LOG=debug npm run tauri dev` for detailed logs.

### Tests

```bash
# Frontend
npm test

# Backend (from src-tauri/)
cargo test
```

---

## Building for production

```bash
npm run tauri build
```

Installers are located in `src-tauri/target/release/bundle/`:
- **Windows:** `nsis/` (NSIS installer) or `msi/` (MSI installer)
- **Linux:** `deb/` (Debian package) or `appimage/` (AppImage)
- **macOS:** `dmg/` (disk image)

### Portable zip (Windows)

After building with `npm run tauri build`:

```powershell
New-Item -ItemType Directory -Path dist\EnergyPy -Force
Copy-Item src-tauri\target\release\energypy_v20.exe, src-tauri\target\release\WebView2Loader.dll dist\EnergyPy\
Compress-Archive -Path dist\EnergyPy -DestinationPath dist\EnergyPy_2.0.1_x64_portable.zip
Remove-Item dist\EnergyPy -Recurse -Force
```

---

## Code conventions

- **Components:** PascalCase (`CpuCard.svelte`)
- **Stores:** camelCase (`system.ts` → `systemStore`)
- **IPC functions:** snake_case in Rust (`get_system_stats`), camelCase in TypeScript (`getSystemStats`)
- **Styles:** Tailwind CSS with custom theme
- **Tests:** Vitest with describe/it blocks in English

---

## Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for recent changes.
