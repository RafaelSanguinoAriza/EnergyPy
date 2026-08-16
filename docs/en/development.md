# 💻 Development Guide — EnergyPy

> **Docs index:** [README](../README.md) · [Installation](installation.md) · [Usage](usage.md) · [Architecture](architecture.md) · [Configuration](configuration.md)

---

## Prerequisites

| Tool | Minimum version | Notes |
|---|---|---|
| [Node.js](https://nodejs.org) | 20+ | Includes npm |
| [Rust](https://www.rust-lang.org/tools/install) | 1.77+ | Install via `rustup` |

### Per-OS dependencies

**Windows**
- Option A (recommended): [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the *"Desktop development with C++"* workload.
- Option B: MSYS2 + MinGW-w64 (GNU toolchain), as used in this project:
  ```
  rustup default stable-x86_64-pc-windows-gnu
  ```
  and make sure `C:\msys64\mingw64\bin` is in your `PATH`.

> ⚠️ **Note (Windows GNU):** this repository is set up for the GNU toolchain.
> MinGW's `ld` overflows the PE export table (error *"export ordinal too
> large"*) when linking Tauri's `cdylib` in debug builds; that is why
> `[profile.dev] opt-level = 2` is configured in `src-tauri/Cargo.toml`. Do not
> remove it if you build with GNU.

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
brew install webkit2gtk  # if needed
```

---

## Project setup

```bash
# Clone the repository
git clone <your-repo>/EnergyPy.git
cd EnergyPy

# Install dependencies
npm install
```

---

## Available scripts

| Command | Description |
|---|---|
| `npm run dev` | Vite dev server (frontend only) |
| `npm run tauri dev` | Full development: frontend + native window with hot reload |
| `npm run build` | Production frontend build |
| `npm run check` | Type checking (svelte-check + TypeScript) |
| `npm test` | Frontend unit tests (Vitest) |
| `cargo test` | Rust backend tests (run in `src-tauri/`) |
| `npm run tauri build` | Build production installers |
| `npm run tauri icon` | Regenerate app icons from a source PNG |

---

## Testing

```bash
npm test                 # Frontend: Vitest (tests/formatters.test.ts)
cargo test               # Backend: run inside src-tauri/
```

- Frontend: covers formatting utilities (`formatBytes`, `formatUptime`,
  `formatTimeRemaining`, `formatDurationShort`, etc.).
- Backend: covers scheduling logic (`seconds_until`), `ActionType` lowercase
  serialization, and admin detection in `power_manager.rs`.

---

## Project structure

```
EnergyPy/
├── src/                          # SvelteKit frontend
│   ├── app.css                   # Tailwind CSS v4 + custom theme
│   ├── app.html                  # HTML template
│   ├── lib/
│   │   ├── components/
│   │   │   ├── dashboard/        # Monitoring cards
│   │   │   ├── power/            # Form + countdown
│   │   │   ├── sidebar/          # Navigation
│   │   │   ├── theme/            # Theme picker
│   │   │   └── ui/               # Base components (Card, Button, etc.)
│   │   ├── i18n/                 # Translations (en.json, es.json)
│   │   ├── stores/               # Svelte stores
│   │   ├── formatters.ts         # Formatting utilities
│   │   ├── tauri.ts              # Tauri command wrappers
│   │   └── update.ts             # Update utility
│   └── routes/                   # Pages (dashboard, power, settings)
├── src-tauri/                    # Rust backend
│   ├── src/
│   │   ├── lib.rs                # Entry point, state, tray, threads
│   │   ├── system_monitor.rs     # System monitoring (sysinfo)
│   │   ├── power_manager.rs      # Power action scheduling
│   │   └── config.rs             # Configuration persistence
│   ├── icons/                    # Generated icons
│   ├── capabilities/             # App permissions
│   ├── Cargo.toml                # Rust dependencies
│   └── tauri.conf.json           # Tauri configuration
├── docs/                         # Documentation (es/en)
├── static/                       # Static assets
├── package.json
└── README.md
```

---

## Typical workflow

1. **Edit the frontend** in `src/` — changes appear instantly in `tauri dev`.
2. **Edit the backend** in `src-tauri/src/` — Tauri recompiles the binary automatically.
3. **Add a new command**:
   - In Rust: `#[tauri::command] fn my_command() { ... }` and add it to the `invoke_handler` in `lib.rs`.
   - In TS: add a wrapper in `src/lib/tauri.ts` using `invoke("my_command", args)`.
   - **Note:** Tauri v2 converts `snake_case` to `camelCase` for arguments (e.g. `action_type` → `actionType`).
4. **Check types:** `npm run check`.
5. **Build:** `npm run tauri build`.

---

## Adding a new language

1. Create `src/lib/i18n/xx.json` with the same keys as `en.json`.
2. In `src/lib/i18n/index.ts`:
   - Import the file: `import xx from "./xx.json";`
   - Add it to the `Record`: `const translations = { en, es, xx };`
   - Add the language to `availableLanguages`.
3. Translate all the app strings.

---

## Logging system

The app uses `log` + `simplelog`. Logs are written to a file:
- **Windows**: `%APPDATA%\EnergyPy\energypy.log`
- **Linux**: `~/.config/EnergyPy/energypy.log`
- **macOS**: `~/Library/Application Support/EnergyPy/energypy.log`

To add logging in Rust:
```rust
log::info!("message");
log::warn!("warning");
log::error!("error");
```

---

## Production build

```bash
npm run tauri build
```

### Outputs (Windows)

| Format | Path |
|---|---|
| Executable | `src-tauri/target/release/energypy_v20.exe` |
| MSI | `src-tauri/target/release/bundle/msi/EnergyPy_2.0.0_x64_en-US.msi` |
| NSIS | `src-tauri/target/release/bundle/nsis/EnergyPy_2.0.0_x64-setup.exe` |

### Regenerating icons

```bash
npm run tauri icon <png-file-1024x1024>
```

---

## Publishing & security

Before publishing the repository or a release:

1. Replace `YOUR_GITHUB_USER` with the real user (`RafaelSanguinoAriza`) in
   `src-tauri/tauri.conf.json` (`plugins.updater.endpoints`).
2. Configure the GitHub secrets `TAURI_SIGNING_PRIVATE_KEY` and
   `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` (see `.github/workflows/release.yml`).
3. Read [SECURITY.md](../../SECURITY.md) — the `.updater-key` file (private
   key) must never be published and is already excluded in `.gitignore`.

---

[← Usage](usage.md) · [Next: Architecture →](architecture.md)