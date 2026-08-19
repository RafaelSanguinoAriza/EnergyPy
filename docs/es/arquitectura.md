# EnergyPy — Arquitectura

Referencia técnica del diseño interno de la aplicación.

---

## Visión general

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
- **Backend:** Rust con `sysinfo` para métricas del sistema.
- **Comunicación:** IPC síncrono/ asíncrono vía `invoke()`.
- **Config:** Archivo JSON persistido por el backend.

---

## Proceso de inicio

1. **`app.html`** — Carga el shell HTML de SvelteKit.
2. **`+layout.server.ts`** — Detecta el idioma del sistema operativo (`platformLocale`).
3. **`+layout.svelte`** — Renderiza sidebar, header y aplica el tema global.
4. **`+page.server.ts`** — Redirige `/` a `/dashboard`.
5. **Dashboard** — Renderiza el Bento Grid con todas las tarjetas (Skeleton loaders se muestran hasta que lleguen los datos).
6. **Backend** — `SystemMonitor::new()` inicializa `sysinfo` con `Components::new_with_refreshed_list()` para temperatura. `PowerManager` crea un `Manager`. Se crea `AppConfig` desde archivo o default. Se inicializa el daemon de energía.
7. **Windows COM** — `CoInitializeEx(COINIT_APARTMENTTHREADED)` se llama al inicio de `run()` para evitar el conflicto `RPC_E_CHANGED_MODE` con `tauri-plugin-notification`.

---

## Backend Rust (src-tauri/)

### Módulos principales

| Módulo | Responsabilidad |
|---|---|
| `lib.rs` | Setup de Tauri + comandos IPC + inicialización COM (Windows) |
| `system_monitor.rs` | Recolección de datos del sistema (CPU con temperatura, memoria, disco, red, batería, procesos) |
| `power_manager.rs` | Control de energía (apagado, reinicio, suspensión, hibernación, bloqueo) |
| `config.rs` | Persistencia de configuración en disco (JSON) |

### Commandos IPC (`lib.rs`)

| Command | Tipo | Descripción |
|---|---|---|
| `get_system_stats` | async | Devuelve `SystemStats` (CPU, memoria, disco, red, batería, uptime, procesos) |
| `get_battery_info` | async | Devuelve `BatteryInfo` por separado |
| `get_process_list` | async | Devuelve `Vec<ProcessInfo>` (hasta 50 procesos con info extendida) |
| `kill_process` | async | Finaliza un proceso por PID (Windows: `taskkill /F /PID`, Linux/macOS: `SIGKILL`) |
| `schedule_power_action` | async | Programa una acción de energía con temporizador |
| `cancel_power_action` | async | Cancela el temporizador activo |
| `get_power_state` | async | Devuelve `PowerState` (temporizador activo, acción, progreso) |
| `execute_power_action` | sync | Ejecuta una acción de energía inmediata |
| `get_config` | async | Lee la configuración actual |
| `save_config` | async | Guarda configuración y aplica cambios (tema, idioma, etc.) |

### Datos del sistema (`SystemStats`)

```rust
pub struct SystemStats {
    pub cpu: CpuInfo,           // Uso, núcleos, frecuencia, uptime, temperatura
    pub memory: MemoryInfo,     // RAM y swap
    pub disk: DiskInfo,         // Lecturas/escrituras, espacio
    pub network: NetworkInfo,   // Interfaces, tráfico
    pub battery: BatteryInfo,   // Nivel, estado, tiempo restante
    pub uptime: u64,            // Tiempo de actividad del sistema
    pub processes: Vec<ProcessInfo>, // Top 50 procesos
}
```

### CpuInfo (con temperatura)

```rust
pub struct CpuInfo {
    pub usage: f32,             // Uso global 0-100%
    pub cores: Vec<f32>,        // Uso por núcleo
    pub frequency: u64,         // Frecuencia en MHz
    pub uptime: u64,            // Tiempo de actividad en segundos
    pub temperature: Option<f32>, // Temperatura en °C (None si no disponible)
}
```

La temperatura se obtiene de `sysinfo::Components`, que se inicializa con `Components::new_with_refreshed_list()` en `SystemMonitor::new()` y se refresca en cada ciclo de `refresh()`.

### ProcessInfo (extendido)

```rust
pub struct ProcessInfo {
    pub pid: u32,
    pub name: String,
    pub cpu_usage: f32,         // Porcentaje 0-100%
    pub memory_usage: f32,      // Porcentaje 0-100%
    pub exe: Option<String>,    // Ruta completa del ejecutable
    pub start_time: Option<u64>, // Timestamp de inicio (epoch seconds)
    pub disk_read: u64,         // Bytes leídos
    pub disk_write: u64,        // Bytes escritos
}
```

### Kill Process

Finaliza un proceso por PID usando el método nativo del sistema operativo:
- **Windows:** `taskkill /F /PID <pid>` (force kill)
- **Linux/macOS:** `libc::kill(pid, SIGKILL)`

---

## Frontend Svelte (src/)

### Stores (Svelte 5 runes)

| Store | Responsabilidad |
|---|---|
| `config.ts` | `AppConfig`: language, theme, notifications, start_minimized, tray_enabled, auto_start, refresh_rate |
| `language.ts` | Idioma actual + traducciones + función `t()` |
| `system.ts` | Datos del sistema: `SystemStats`, `CpuInfo`, `MemoryInfo`, `DiskInfo`, `NetworkInfo`, `BatteryInfo`, `ProcessInfo` |
| `power.ts` | Estado de energía: temporizador, acción activa, progreso |
| `toast.ts` | Cola de notificaciones toast (success, error, warning, info) |

### Funciones IPC (TypeScript)

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

### Transiciones

Las páginas se animan con `in:fly`/`out:fly` bidireccionales:
- Entrada: `x: 30 → 0`, duración 250ms, delay 100ms
- Salida: `x: 0 → -30`, duración 200ms

Las filas de procesos usan `transition:fade` con duración 120ms.

---

## Persistencia

| Dato | Almacén | Formato |
|---|---|---|
| Configuración | Archivo JSON en directorio de config | `AppConfig` serializado |
| Logs | Archivos rotativos | Texto plano |
| No hay base de datos | — | — |

---

## Rendimiento

- **Backend:** `sysinfo` actualiza métricas en cada invoke (~100ms por consulta).
- **Frontend:** Polling configurable (default 2s, rango 1-10s) con `setInterval`.
- **Memoria:** ~50 MB en ejecución normal.
- **CPU:** <1% en estado idle.
- **Skeleton loaders:** Se muestran inmediatamente mientras llegan los datos reales.
- **Toast notifications:** Auto-dismiss con animación, sin bloquear la interfaz.

---

## Seguridad

- **IPC whitelist:** Solo los commands definidos en `tauri.conf.json` están expuestos.
- **Permisos:** Tauri v2 usa un sistema de permisos granular por plugin.
- **No hay servidor web:** La app no expone puertos ni endpoints HTTP.
- **Kill process:** Requiere confirmación del usuario antes de ejecutar.

---

## Changelog

Consulta [CHANGELOG.md](../../CHANGELOG.md) para los cambios recientes.
