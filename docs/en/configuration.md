# EnergyPy — Configuration

Detailed reference for configuration options and system files.

---

## Configuration file

Configuration is stored in a JSON file in the system's config directory:

| System | Location |
|---|---|
| **Windows** | `%APPDATA%/EnergyPy/config.json` |
| **Linux** | `~/.config/EnergyPy/config.json` |
| **macOS** | `~/Library/Application Support/EnergyPy/config.json` |

---

## Configuration options

### `language`

- **Type:** `string`
- **Values:** `"en"` (English), `"es"` (Español)
- **Default:** Detected from the OS (`navigator.language`)
- **Description:** User interface language.

### `theme`

- **Type:** `string`
- **Values:** `"light"`, `"dark"`, `"system"`
- **Default:** `"system"`
- **Description:** Application visual theme. `"system"` follows the OS preference.

### `notifications`

- **Type:** `boolean`
- **Default:** `true`
- **Description:** Enables or disables system notifications (toast notifications).

### `start_minimized`

- **Type:** `boolean`
- **Default:** `false`
- **Description:** When `true`, the application starts minimized in the system tray.

### `tray_enabled`

- **Type:** `boolean`
- **Default:** `true`
- **Description:** When `true`, the application minimizes to the system tray when the window is closed.

### `auto_start`

- **Type:** `boolean`
- **Default:** `false`
- **Description:** When `true`, the application runs automatically when the OS boots. Uses the Tauri autostart plugin to register/unregister the app with the system.

### `refresh_rate`

- **Type:** `integer`
- **Range:** 1 - 10
- **Default:** `2`
- **Unit:** Seconds
- **Description:** Dashboard and system data update interval. Lower values provide more frequent updates but use more CPU.

---

## Example configuration file

```json
{
  "language": "es",
  "theme": "dark",
  "notifications": true,
  "start_minimized": false,
  "tray_enabled": true,
  "auto_start": false,
  "refresh_rate": 2
}
```

---

## Default configuration

If the configuration file doesn't exist or is corrupted, the default configuration is used:

```json
{
  "language": "system",
  "theme": "system",
  "notifications": true,
  "start_minimized": false,
  "tray_enabled": true,
  "auto_start": false,
  "refresh_rate": 2
}
```

---

## Build parameters

### `Cargo.toml` (Backend)

| Field | Value |
|---|---|
| `name` | `energypy` |
| `version` | `2.0.1` |
| `description` | "Cross-platform desktop power and system monitor" |
| `authors` | `["Rafael David Sanguino Ariza"]` |
| `edition` | `2021` |

### `tauri.conf.json`

| Field | Value |
|---|---|
| `identifier` | `com.energypy.app` |
| `productName` | `EnergyPy` |
| `version` | `2.0.1` |
| `title` | `⚡ EnergyPy v2.0.1` |
| `width` | `1100` |
| `height` | `750` |
| `minWidth` | `900` |
| `minHeight` | `600` |
| `decorations` | `true` |
| `transparent` | `false` |
| `resizable` | `true` |
| `fullscreen` | `false` |
| `log level` | `debug` (dev) / `info` (prod) |

### `package.json` (Frontend)

| Field | Value |
|---|---|
| `name` | `energypy-v2` |
| `version` | `2.0.1` |
| `description` | "Cross-platform desktop power and system monitor" |
| `svelte` | `^5.35.5` |
| `@tauri-apps/api` | `^2.8.0` |
| `@tauri-apps/plugin-autostart` | `^2.5.0` |
| `@tauri-apps/plugin-shell` | `^2.3.0` |
| `lucide-svelte` | `^0.544.0` |
| `tailwindcss` | `^4.1.13` |

---

## Logs

| System | Location |
|---|---|
| **Development** | `logs/energy_py.log` |
| **Production** | System config directory |

### Log level

- **Development:** `Debug` (everything included)
- **Production:** `Info` (information and errors only)

### Configuring log level

```bash
# Verbose debug
RUST_LOG=debug npm run tauri dev

# Errors only
RUST_LOG=error npm run tauri dev
```

---

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+C` | Cancel active power timer |
| `Ctrl+T` | Toggle theme (light / dark / system) |
| `Ctrl+Q` | Exit application |

---

## Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for recent changes.
