# 🏗️ Architecture — EnergyPy

> **Docs index:** [README](../README.md) · [Installation](installation.md) · [Usage](usage.md) · [Development](development.md) · [Configuration](configuration.md)

---

## Overview

EnergyPy uses a **hybrid architecture**:

- **Frontend**: SvelteKit 5 + TypeScript (SPA) rendered in a WebView.
- **Backend**: native Rust compiled to a binary, communicating with the frontend via **IPC** (command invoke + events).

```
┌────────────────────────────────────┐
│           SvelteKit (WebView)      │
│  UI · Stores · i18n · Components   │
└──────────────┬─────────────────────┘
               │  IPC (invoke / events)
┌──────────────▼─────────────────────┐
│            Tauri Core (Rust)       │
│  SystemMonitor · PowerManager      │
│  Config · Tray · Plugins · Threads │
└────────────────────────────────────┘
```

---

## Frontend layer (SvelteKit)

### Tauri communication

All commands are exposed in `src/lib/tauri.ts`:

| TS function | Rust command | Description |
|---|---|---|
| `getSystemStats()` | `get_system_stats` | System statistics |
| `scheduleShutdown()` | `schedule_shutdown` | Schedule a power action |
| `scheduleAtTime()` | `schedule_at_time` | Schedule at an exact hour |
| `cancelShutdown()` | `cancel_shutdown` | Cancel the scheduled action |
| `getScheduledAction()` | `get_scheduled_action` | Countdown state |
| `getConfig()` | `get_config` | Saved configuration |
| `saveConfig()` | `save_config` | Persist configuration |
| `exitApp()` | `exit_app` | Quit the app |
| `requiresAdmin()` | `requires_admin` | Check admin privileges |

### Backend events

| Event | Frequency | Payload |
|---|---|---|
| `system-stats` | every 2 s | Full `SystemStats` |
| `countdown-tick` | every 1 s | `ScheduledAction` (progress) |

### Svelte stores

| Store | Content |
|---|---|
| `systemStats` | Latest stats reading |
| `cpuHistory` | CPU history (60 samples) |
| `scheduledAction` | Countdown state |
| `appConfig` | Reactive configuration |
| `theme` | Theme preference |
| `resolvedTheme` | Effective theme (after resolving "system") |
| `currentLang` | Active language |

### i18n system

`src/lib/i18n/index.ts` defines a derived store `t`:

```ts
export const t = derived(currentLang, ($lang) => (key, params?) => { ... });
```

- Dictionaries live in `en.json` and `es.json`.
- Keys are **flat** (no prefixes).
- Use `{$t("key")}` in templates; wrap in `$derived` for reactivity in `<script>`.

---

## Backend layer (Rust)

### Modules

| Module | Responsibility |
|---|---|
| `lib.rs` | Entry point, global state, tray, emitter threads |
| `system_monitor.rs` | Reading system metrics (crate `sysinfo`) |
| `power_manager.rs` | Scheduling and executing power actions |
| `config.rs` | Loading/saving configuration to disk |

### `system_monitor.rs`

Uses the **sysinfo** crate for:

- **CPU**: global and per-core usage, frequency, brand.
- **Memory**: total, used, available, swap.
- **Disks**: partitions with used/total space.
- **Network**: computes **speed** as a differential between measurements (saving previous values before each refresh).
- **Battery**:
  - Windows: `wmic` (run silently).
  - Linux: reading `/sys/class/power_supply/BAT*` (supports `BAT0`, `BAT1`, etc.).
  - macOS: `pmset -g batt`.
- **Processes**: top 10 by CPU usage.

### `power_manager.rs`

Keeps the scheduled action state plus an **atomic generation token** (`AtomicU64`):

- `schedule(seconds, action)` — increments the generation and spawns a thread that sleeps `seconds`.
- The thread, before executing, **verifies the generation hasn't changed** (not cancelled or replaced).
- `cancel()` — increments the generation (invalidates pending threads) and runs the OS abort command.
- `schedule_at_time()` — computes the delta to the target hour (if already passed, schedules for the next day).

This guarantees that cancelling an action **really aborts** the scheduled shutdown/restart.

### `config.rs`

- Saves config as JSON in:
  - Windows: `%APPDATA%\EnergyPy\config.json`
  - Linux: `~/.config/EnergyPy/config.json`
  - macOS: `~/Library/Application Support/EnergyPy/config.json`
- If the file is missing or invalid, returns default values.

### `lib.rs`

- Initializes the logger (`simplelog`) writing to `energypy.log` in the same config directory.
- Configures **plugins**: opener, notification, shell, autostart, process, single-instance, dialog, updater.
- Creates the **system tray** (menu: Show / Quit; click restores the window).
- Spawns **two emitter threads**: `system-stats` (2 s) and `countdown-tick` (1 s).

---

## Security and external processes

All external commands (`shutdown`, `rundll32`, `wmic`, `systemctl`, `pmset`, `loginctl`) run **silently**:

- `stdout`/`stderr` redirected to null or piped (no console).
- On Windows, the `CREATE_NO_WINDOW` flag (0x08000000) is used to **prevent a console from flashing**.
- This fix was applied in v2.0.0 (`power_manager.rs` and `system_monitor.rs`).

The release binary uses `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]`, preventing a console window in production.

---

## Data flow (example: scheduling a shutdown)

1. The user clicks "Schedule" in the form.
2. `ScheduleForm.svelte` confirms via a dialog and calls `scheduleShutdown(seconds, actionType)`.
3. Tauri IPC invokes `schedule_shutdown` in Rust.
4. `PowerManager::schedule()` stores the action and spawns the thread.
5. Every second, `countdown-tick` emits the progress → updates the countdown in the UI.
6. If the user cancels, `cancel()` invalidates the thread and runs `shutdown /a`.

---

[← Development](development.md) · [Next: Configuration →](configuration.md)