# 🏗️ Arquitectura — EnergyPy

> **Índice de docs:** [README](../README.md) · [Instalación](instalacion.md) · [Uso](uso.md) · [Desarrollo](desarrollo.md) · [Configuración](configuracion.md)

---

## Visión general

EnergyPy es una aplicación de **arquitectura híbrida**:

- **Frontend**: SvelteKit 5 + TypeScript (SPA) renderizado en un WebView.
- **Backend**: Rust nativo compilado a binario, comunicándose con el frontend vía **IPC** (invoke de comandos + eventos).

```
┌────────────────────────────────────┐
│           SvelteKit (WebView)      │
│  UI · Stores · i18n · Componentes  │
└──────────────┬─────────────────────┘
               │  IPC (invoke / events)
┌──────────────▼─────────────────────┐
│            Tauri Core (Rust)       │
│  SystemMonitor · PowerManager      │
│  Config · Tray · Plugins · Threads │
└────────────────────────────────────┘
```

---

## Capa de frontend (SvelteKit)

### Comunicación con Tauri

Todos los comandos se exponen en `src/lib/tauri.ts`:

| Función TS | Comando Rust | Descripción |
|---|---|---|
| `getSystemStats()` | `get_system_stats` | Estadísticas del sistema |
| `scheduleShutdown()` | `schedule_shutdown` | Programa acción de energía |
| `scheduleAtTime()` | `schedule_at_time` | Programa a hora exacta |
| `cancelShutdown()` | `cancel_shutdown` | Cancela acción programada |
| `getScheduledAction()` | `get_scheduled_action` | Estado del countdown |
| `getConfig()` | `get_config` | Configuración guardada |
| `saveConfig()` | `save_config` | Persiste configuración |
| `exitApp()` | `exit_app` | Cierra la app |
| `requiresAdmin()` | `requires_admin` | Verifica privilegios admin |

### Eventos del backend

| Evento | Frecuencia | Datos |
|---|---|---|
| `system-stats` | cada 2 s | `SystemStats` completo |
| `countdown-tick` | cada 1 s | `ScheduledAction` (progreso) |

### Stores de Svelte

| Store | Contenido |
|---|---|
| `systemStats` | Última lectura de estadísticas |
| `cpuHistory` | Historial de CPU (60 muestras) |
| `scheduledAction` | Estado del countdown |
| `appConfig` | Configuración reactiva |
| `theme` | Preferencia de tema |
| `resolvedTheme` | Tema efectivo (tras resolver "system") |
| `currentLang` | Idioma activo |

### Sistema i18n

`src/lib/i18n/index.ts` define un store derivado `t`:

```ts
export const t = derived(currentLang, ($lang) => (key, params?) => { ... });
```

- Los diccionarios viven en `en.json` y `es.json`.
- Las claves son **planas** (sin prefijos).
- El uso en componentes es `{$t("clave")}`; en `<script>` reactivo se envuelve en `$derived`.

---

## Capa de backend (Rust)

### Módulos

| Módulo | Responsabilidad |
|---|---|
| `lib.rs` | Entry point, estado global, bandeja, threads de emisión |
| `system_monitor.rs` | Lectura de métricas del sistema (crate `sysinfo`) |
| `power_manager.rs` | Lógica de programación y ejecución de acciones |
| `config.rs` | Carga/guardado de configuración en disco |

### `system_monitor.rs`

Usa el crate **sysinfo** para:

- **CPU**: uso global y por núcleo, frecuencia, marca.
- **Memoria**: total, usada, disponible, swap.
- **Discos**: particiones con espacio usado/total.
- **Red**: calcula **velocidad** como diferencial entre mediciones (guardando valores previos antes de cada refresh).
- **Batería**:
  - Windows: `wmic` (ejecutado silenciosamente).
  - Linux: lectura de `/sys/class/power_supply/BAT*` (soporta `BAT0`, `BAT1`, etc.).
  - macOS: `pmset -g batt`.
- **Procesos**: top 10 por uso de CPU.

### `power_manager.rs`

Mantiene el estado de la acción programada y un **token de generación atómico** (`AtomicU64`):

- `schedule(seconds, action)` — incrementa la generación y lanza un thread que duerme `seconds`.
- El thread, antes de ejecutar la acción, **verifica que la generación no haya cambiado** (no fue cancelada ni reemplazada).
- `cancel()` — incrementa la generación (invalida threads pendientes) y ejecuta el comando de aborto del SO.
- `schedule_at_time()` — calcula el delta hasta la hora objetivo (si ya pasó, programa para el día siguiente).

Esto garantiza que cancelar una acción **aborta de verdad** el apagado/reinicio programado.

### `config.rs`

- Guarda la configuración como JSON en:
  - Windows: `%APPDATA%\EnergyPy\config.json`
  - Linux: `~/.config/EnergyPy/config.json`
  - macOS: `~/Library/Application Support/EnergyPy/config.json`
- Si el archivo no existe o es inválido, devuelve los valores predeterminados.

### `lib.rs`

- Inicializa el logger (`simplelog`) escribiendo a `energypy.log` en el mismo directorio de la config.
- Configura **plugins**: opener, notification, shell, autostart, process, single-instance, dialog, updater.
- Crea la **bandeja del sistema** (menú: Mostrar / Salir; clic restaura la ventana).
- Lanza **dos threads de emisión**: `system-stats` (2 s) y `countdown-tick` (1 s).

---

## Seguridad y procesos externos

Todos los comandos externos (`shutdown`, `rundll32`, `wmic`, `systemctl`, `pmset`, `loginctl`) se ejecutan **silenciosamente**:

- `stdout`/`stderr` redirigidos a null o piped (sin consola).
- En Windows, con el flag `CREATE_NO_WINDOW` (0x08000000) para **evitar que parpadee una consola**.
- Esta corrección se aplicó en v2.0.0 (módulos `power_manager.rs` y `system_monitor.rs`).

El binario de release usa `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]`, que evita la ventana de consola en producción.

---

## Flujo de datos (ejemplo: programar apagado)

1. Usuario hace clic en "Programar" en el formulario.
2. `ScheduleForm.svelte` confirma con diálogo y llama `scheduleShutdown(seconds, actionType)`.
3. Tauri IPC invoca `schedule_shutdown` en Rust.
4. `PowerManager::schedule()` almacena la acción y lanza el thread.
5. Cada segundo, `countdown-tick` emite el progreso → actualiza el countdown en la UI.
6. Si el usuario cancela, `cancel()` invalida el thread y ejecuta `shutdown /a`.

---

[← Desarrollo](desarrollo.md) · [Siguiente: Configuración →](configuracion.md)