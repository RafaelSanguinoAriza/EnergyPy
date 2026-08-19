# EnergyPy — Architecture

Technical reference for the application's internal design.

---

## Overview

```
┌─────────────────────────────────────────────────┐
│                  EnergyPy                         │
├────────────────────┬────────────────────────────┤
│   Frontend (Web)   │      Backend (Rust)         │
│   SvelteKit 5 +    │      sysinfo + Tauri        │
│   TypeScript        │      IPC Commands           │
└────────┬───────────┴──────────────┬─────────────┘
         │ invoke()                 │ tauri::command
         │                          │
         │  system_monitor.rs       │  ⇅ JSON
         │  power_manager.rs        │
         │  config.rs               │
         └──────────────────────────┘
```

- **Frontend:** SvelteKit + TypeScript + Tailwind CSS + Lucide.
- **Backend:** Rust with `sysinfo` for system metrics.
- **Communication:** Synchronous/asynchronous IPC via `invoke()`.
- **Config:** JSON file persisted by the backend.

---

## Startup process

1. **`app.html`** — Loads the SvelteKit HTML shell.
2. **`+layout.server.ts`** — Detects the OS language (`platformLocale`).
3. **`+layout.svelte`** — Renders sidebar, header and applies the global theme.
4. **`+page.server.ts`** — Redirects `/` to `/dashboard`.
5. **Dashboard** — Renders the Bento Grid with all cards (Skeleton loaders display until data arrives).
6. **Backend** — `SystemMonitor::new()` initializes `sysinfo` with `Components::new_with_refreshed_list()` for temperature. `PowerManager` creates a `Manager`. `AppConfig` is created from file or default. The power daemon is initialized.
7. **Windows COM** — `CoInitializeEx(COINIT_APARTMENTTHREADED)` is called at the start of `run()` to prevent the `RPC_E_CHANGED_MODE` conflict with `tauri-plugin-notification`.

---

## Rust Backend (src-tauri/)

### Main modules

| Module | Responsibility |
|---|---|
| `lib.rs` | Tauri setup + IPC commands + COM initialization (Windows) |
| `system_monitor.rs` | System data collection (CPU with temperature, memory, disk, network, battery, processes) |
| `power_manager.rs` | Power control (shutdown, restart, suspend, hibernate, lock) |
| `config.rs` | Configuration persistence (JSON file) |

### IPC Commands (`lib.rs`)

| Command | Type | Description |
|---|---|---|
| `get_system_stats` | async | Returns `SystemStats` (CPU, memory, disk, network, battery, uptime, processes) |
| `get_battery_info` | async | Returns `BatteryInfo` separately |
| `get_process_list` | async | Returns `Vec<ProcessInfo>` (up to 50 processes with extended info) |
| `kill_process` | async | Terminates a process by PID (Windows: `taskkill /F /PID`, Linux/macOS: `SIGKILL`) |
| `schedule_power_action` | async | Schedules a power action with timer |
| `cancel_power_action` | async | Cancels the active timer |
| `get_power_state` | async | Returns `PowerState` (active timer, action, progress) |
| `execute_power_action` | sync | Executes an immediate power action |
| `get_config` | async | Reads current configuration |
| `save_config` | async | Saves configuration and applies changes (theme, language, etc.) |

### System data (`SystemStats`)

```rust
pub struct SystemStats {
    pub cpu: CpuInfo,           // Usage, cores, frequency, uptime, temperature
    pub memory: MemoryInfo,     // RAM and swap
    pub disk: DiskInfo,         // Reads/writes, space
    pub network: NetworkInfo,   // Interfaces, traffic
    pub battery: BatteryInfo,   // Level, status, time remaining
    pub uptime: u64,            // System uptime in seconds
    pub processes: Vec<ProcessInfo>, // Top 50 processes
}
```

### CpuInfo (with temperature)

```rust
pub struct CpuInfo {
    pub usage: f32,             // Overall usage 0-100%
    pub cores: Vec<f32>,        // Per-core usage
    pub frequency: u64,         // Frequency in MHz
    pub uptime: u64,            // Uptime in seconds
    pub temperature: Option<f32>, // Temperature in °C (None if unavailable)
}
```

Temperature is obtained from `sysinfo::Components`, initialized with `Components::new_with_refreshed_list()` in `SystemMonitor::new()` and refreshed in each `refresh()` cycle.

### ProcessInfo (extended)

```rust
pub struct ProcessInfo {
    pub pid: u32,
    pub name: String,
    pub cpu_usage: f32,         // Percentage 0-100%
    pub memory_usage: f32,      // Percentage 0-100%
    pub exe: Option<String>,    // Full executable path
    pub start_time: Option<u64>, // Start timestamp (epoch seconds)
    pub disk_read: u64,         // Bytes read
    pub disk_write: u64,        // Bytes written
}
```

### Kill Process

Terminates a process by PID using the OS-native method:
- **Windows:** `taskkill /F /PID <pid>` (force kill)
- **Linux/macOS:** `libc::kill(pid, SIGKILL)`

---

## Svelte Frontend (src/)

### Stores (Svelte 5 runes)

| Store | Responsibility |
|---|---|
| `config.ts` | `AppConfig`: language, theme, notifications, start_minimized, tray_enabled, auto_start, refresh_rate |
| `language.ts` | Current language + translations + `t()` function |
| `system.ts` | System data: `SystemStats`, `CpuInfo`, `MemoryInfo`, `DiskInfo`, `NetworkInfo`, `BatteryInfo`, `ProcessInfo` |
| `power.ts` | Power state: timer, active action, progress |
| `toast.ts` | Toast notification queue (success, error, warning, info) |

### IPC Functions (TypeScript)

```typescript
// system.ts
getSystemStats()    → Promise<SystemStats>
getBatteryInfo()    → Promise<BatteryInfo>
getProcessList()    → Promise<ProcessInfo[]>
killProcess(pid)    → Promise<void>

// power.ts
schedulePowerAction(action, hours, minutes, seconds) → Promise<void>
cancelPowerAction()   → Promise<void>
getPowerState()       → Promise<PowerState>
executePowerAction()  → Promise<void>

// config.ts
getConfig()    → Promise<AppConfig>
saveConfig()   → Promise<void>

// autostart.ts (Tauri plugins)
enableAutostart()      → Promise<void>
disableAutostart()     → Promise<void>
isEnabledAutostart()   → Promise<boolean>
```

### Routing (SvelteKit)

```
/                  → redirect to /dashboard
/dashboard         → Bento Grid (CPU, Memory, Disk, Network, SystemInfo, HealthBar, ProcessList)
/processes         → Process manager (table, search, sort, kill)
/power             → Power control (scheduling + manual execution)
/settings          → Settings (language, theme, notifications, autostart, refresh rate, about)
```

### Transitions

Pages animate with bidirectional `in:fly`/`out:fly`:
- Enter: `x: 30 → 0`, duration 250ms, delay 100ms
- Exit: `x: 0 → -30`, duration 200ms

Process rows use `transition:fade` with 120ms duration.

---

## Persistence

| Data | Store | Format |
|---|---|---|
| Configuration | JSON file in system config directory | Serialized `AppConfig` |
| Logs | Rotating files | Plain text |
| No database | — | — |

---

## Performance

- **Backend:** `sysinfo` refreshes metrics on each invoke (~100ms per query).
- **Frontend:** Configurable polling (default 2s, range 1-10s) with `setInterval`.
- **Memory:** ~50 MB during normal operation.
- **CPU:** <1% when idle.
- **Skeleton loaders:** Display immediately while real data arrives.
- **Toast notifications:** Auto-dismiss with animation, non-blocking.

---

## Security

- **IPC whitelist:** Only commands defined in `tauri.conf.json` are exposed.
- **Permissions:** Tauri v2 uses a granular per-plugin permission system.
- **No web server:** The app doesn't expose ports or HTTP endpoints.
- **Kill process:** Requires user confirmation before execution.

---

## Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for recent changes.
