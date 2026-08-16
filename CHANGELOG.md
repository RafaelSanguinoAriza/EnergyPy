# Changelog

## [Unreleased] - 2026-08-16

### Added
- **KPI strip** — new `SystemHealthBar` on the dashboard showing compact CPU, memory, disk, and battery readouts with color-coded progress bars and "—" placeholders when data is unavailable.
- **System info card** — new `SystemInfoCard` on the dashboard showing OS, kernel, hostname, architecture, and uptime; backend now reports `arch` (`SystemStats.arch`).

### Changed
- **Dashboard layout** — reflowed grid: KPI strip on top; row 2 = Disk (2 cols) + Network + Battery; row 3 = Uptime + System; row 4 = top processes full width.
- **Dark theme palette** — replaced pure-gray dark mode with a slate blue-gray palette (`slate-900` background, `slate-800` cards, `slate-700` surfaces, `slate-600` tracks/borders) across all components and pages.
- **Number inputs** — native spinner arrows hidden via CSS (`appearance: none` / `::-webkit-inner-spin-button`) while keeping `type="number"` validation.
- **Installer branding** — `bundle` metadata added (`publisher`, `category`, `shortDescription`, `longDescription`, `copyright`); custom NSIS header/sidebar images and MSI banner/dialog images (generated in `src-tauri/bundle-images/`); NSIS installer now bilingual (English + Spanish with language selector) and installs per-user (`currentUser`).

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
