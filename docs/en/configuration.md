# ⚙️ Configuration — EnergyPy

> **Docs index:** [README](../README.md) · [Installation](installation.md) · [Usage](usage.md) · [Development](development.md) · [Architecture](architecture.md)

---

## Configuration file

EnergyPy stores its preferences in a JSON file. Location per OS:

| System | Path |
|---|---|
| **Windows** | `%APPDATA%\EnergyPy\config.json` |
| **Linux** | `~/.config/EnergyPy/config.json` |
| **macOS** | `~/Library/Application Support/EnergyPy/config.json` |

Configuration is loaded automatically on startup and saved when pressing **"Save settings"** in the Settings section.

---

## Options

### `theme`
Interface theme.

| Value | Effect |
|---|---|
| `"light"` | Light theme |
| `"dark"` | Dark theme |
| `"system"` | Follows the OS (default) |

### `language`
Interface language.

| Value | Effect |
|---|---|
| `"en"` | English |
| `"es"` | Spanish |

### `notifications_enabled`
Boolean. Enables/disables system notifications.

### `minimize_to_tray`
Boolean. When `true`, closing the window hides the app to the tray instead of exiting.

### `start_minimized`
Boolean. When `true`, the app starts hidden in the tray.

### `auto_update`
Boolean. When `true`, the app checks and applies updates automatically.

### `last_tab`
String. Last visited section (`"dashboard"`, `"power"`, `"settings"`).

---

## Example file

```json
{
  "theme": "system",
  "language": "es",
  "notifications_enabled": true,
  "minimize_to_tray": true,
  "start_minimized": false,
  "auto_update": true,
  "last_tab": "dashboard"
}
```

---

## Log file

The activity log (`energypy.log`) lives in the same directory as `config.json`:

| System | Path |
|---|---|
| **Windows** | `%APPDATA%\EnergyPy\energypy.log` |
| **Linux** | `~/.config/EnergyPy/energypy.log` |
| **macOS** | `~/Library/Application Support/EnergyPy/energypy.log` |

---

## Packaging configuration (`tauri.conf.json`)

File at `src-tauri/tauri.conf.json`:

| Key | Description |
|---|---|
| `productName` | Product name (`EnergyPy`) |
| `version` | App version (`2.0.0`) |
| `identifier` | Unique identifier (`com.energypy.desktop`) |
| `app.windows` | Window configuration (size, title, centering) |
| `bundle.icon` | Per-platform icons |
| `plugins.updater` | Update endpoint and public key |

---

## Permissions (`capabilities/default.json`)

Defines app permissions for each Tauri plugin:

- **opener**: open URLs in the external browser.
- **notification**: send notifications.
- **shell**: run commands / open files.
- **autostart**: start with the system.
- **process**: exit / restart the process.
- **dialog**: native dialogs (confirmation).
- **updater**: check and download updates.
- **core:event**: subscribe to events (stats, countdown).

---

[← Architecture](architecture.md) · [Back to index](../README.md)