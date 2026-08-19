# Changelog

## [2.0.1] - 2026-08-17

### Added
- **Process Manager** — new `/processes` route with a full-featured process table: search by name/PID, column sort (name, CPU%, memory, Mem%), per-process kill with confirmation dialog, kill-all-filtered button, and 50-process limit (increased from 10).
- **Extended process info** — process table now shows executable path, process uptime, and disk read/write bytes.
- **CPU temperature** — `CpuCard` displays real-time temperature via `sysinfo::Components` with color thresholds (green < 65°C, yellow < 85°C, red ≥ 85°C).
- **Auto-start with system** — new `auto_start` config option in Settings; uses `tauri-plugin-autostart` to register/unregister OS-level autostart.
- **Configurable refresh rate** — new `refresh_rate` config option (1–10 s, default 2 s); the backend stats emission thread reads the value dynamically.
- **Skeleton loaders** — all dashboard cards (`CpuCard`, `MemoryCard`, `DiskCard`, `NetworkCard`, `SystemInfoCard`, `SystemHealthBar`) and `ProcessTable` show shimmer-animated skeletons instead of "Loading..." text while data is unavailable.
- **Toast notifications** — reusable toast system (`toast.ts` store + `Toast.svelte` component) with success/error/warning/info variants, auto-dismiss, and close button; integrated in the root layout and shown on settings save/reset and errors.
- **About section in Settings** — displays app description, version, license, and a clickable link to the author's GitHub profile.
- **Bidirectional page transitions** — navigation between tabs uses `in:fly`/`out:fly` (left/right) for a natural directional feel.

### Changed
- **Dashboard bento grid** — reorganized layout: CPU (3 cols) + SystemInfo (1 col) on row 1; Memory (2 cols) + Network (2 cols) on row 2; Disk (2 cols) + SystemHealthBar (2 cols) on row 3; ProcessList (4 cols, compact 5 processes with "View all →" link) on row 4.
- **KPI strip** — new `SystemHealthBar` showing compact CPU, memory, disk, and battery readouts with color-coded progress bars.
- **System info card** — `SystemInfoCard` now shows uptime prominently, plus OS, kernel, hostname, and architecture.
- **Process row transitions** — table rows use `transition:fade` (120 ms) for smooth appear/disappear when filtering or sorting.
- **Process table scroll** — fixed-height scroll container (`max-h-[500px]`) with sticky thead and custom scrollbar styling.
- **Dark theme palette** — pure-gray dark mode replaced with slate blue-gray palette across all components.
- **Number inputs** — native spinner arrows hidden via CSS while keeping `type="number"` validation.
- **Installer branding** — `bundle` metadata, custom NSIS header/sidebar images, bilingual NSIS installer.
- **Version** — bumped to 2.0.1 across package.json, Cargo.toml, and tauri.conf.json.
- **Project metadata** — updated Cargo.toml description and authors; added description to package.json.

### Fixed
- **Windows COM panic** — `RPC_E_CHANGED_MODE` crash on startup caused by `tauri-plugin-notification` initializing COM in MTA mode before WebView2's STA requirement; fixed by calling `CoInitializeEx(COINIT_APARTMENTTHREADED)` before Tauri builder.
- **Dark mode process table** — fixed `slate-750` (non-existent Tailwind class) → `slate-700`.
- **Missing i18n keys** — added `about_description`, `author`, `github_profile`, `start_time` keys that were referenced in components but missing from translation files.
- **Empty `handleScheduled`** — removed dead function from `power/+page.svelte`.

### Removed
- **`UptimeCard.svelte`** — consolidated into `SystemInfoCard`.
- **`BatteryCard.svelte`** — battery info merged into `SystemHealthBar`.
- **`cpuHistory` store** — removed dead store and chart.js dependency.

## [Unreleased]

_No unreleased changes beyond 2.0.1._

## [2.0.0] - 2026-06-14

### Added
- **System Monitoring Dashboard** — Real-time CPU, memory, disk, network, uptime, and battery monitoring with live updates every 2 seconds.
- **Power Control** — Schedule shutdown, restart, suspend, hibernate, and lock actions with countdown timer and progress bar.
- **Multi-language Support** — English and Spanish interface with seamless language switching via i18n.
- **Theme Support** — Light, dark, and system-following theme with persistent preference.
- **Keyboard Shortcuts** — Ctrl+C (cancel action), Ctrl+T (toggle theme), Ctrl+Q (quit).
- **System Tray** — Background operation with tray icon and quick-action menu.
- **Auto-Update Ready** — Framework set up for automatic updates via GitHub Releases.
- **Single Instance** — Prevents duplicate application launches.
- **Desktop Installers** — MSI and NSIS Windows installers with custom EnergyPy branding.

### Fixed (QA pass)
- **Scheduled actions** — `schedule_at_time` now runs immediately (0 s) when the target time equals the current time; the scheduled state is cleared after execution; a `power-action-result` event is emitted to the frontend.
- **Admin detection** — `requires_admin` command renamed to `is_admin` with correct semantics (returns `true` when the user *is* admin) and proper per-OS checks (Windows: S-1-16-12288 elevation, Unix: uid 0).
- **Battery reporting** — Windows battery read via PowerShell `Get-CimInstance Win32_Battery` (removed deprecated `wmic`); real battery presence detection; remaining/full times converted to **seconds** consistently across OSes.
- **Network interfaces** — `refresh(true)` discards stale interfaces on refresh.
- **Theme** — "System" theme now reacts live to `prefers-color-scheme` changes.
- **Keyboard shortcuts** — Ctrl+C/Ctrl+T/Ctrl+Q are ignored when the focus is on an input field.
- **Last tab restore** — the last visited tab is restored on launch and persisted on navigation.
- **Auto-update** — frontend now uses the plugin correctly (single `check` + `downloadAndInstall(update)`); shown on startup when enabled.
- **Notifications** — `power-action-result` listener shows a native notification when enabled.
- **Window behavior** — `minimize_to_tray`/`start_minimized` respected; `CloseRequested` exits when minimize-to-tray is off.
- **Config robustness** — `load_config` merges partial/invalid JSON, keeping valid fields.
- **Unit display** — Countdown timer, battery card, and schedule form use the correct time units (`formatDurationShort`) and translated action labels.
- **Toggle component** — rewritten with Svelte 5 runes (no prop mutation), keyboard + ARIA accessible.
- **Dead code removed** — unused `Modal.svelte`, `chart.js` dependency, and `cpuHistory` store.
- **CSP** — restrictive Content-Security-Policy added to `tauri.conf.json`.
- **Tests** — Vitest added (16 frontend unit tests) and Rust unit tests for `power_manager.rs` (schedule/`seconds_until`/serialization).

### Technical
- Built with Tauri v2 + SvelteKit 5 + TypeScript + Tailwind CSS v4.
- Svelte 5 runes (`$state`, `$derived`, `$effect`, `$bindable`) for reactive architecture.
- Rust backend with `sysinfo` crate for cross-platform system monitoring.
- Real battery detection (Windows, Linux, macOS).
- Custom EnergyPy icon set generated for all platforms (Windows, macOS, Linux, iOS, Android).
- Page transition animations with Svelte `fly` transition.
- EnergyPy brand identity with green gradient color palette.
