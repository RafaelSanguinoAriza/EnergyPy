# EnergyPy — Configuración

Referencia detallada de las opciones de configuración y archivos del sistema.

---

## Archivo de configuración

La configuración se almacena en un archivo JSON en el directorio de configuración del sistema:

| Sistema | Ubicación |
|---|---|
| **Windows** | `%APPDATA%/EnergyPy/config.json` |
| **Linux** | `~/.config/EnergyPy/config.json` |
| **macOS** | `~/Library/Application Support/EnergyPy/config.json` |

---

## Opciones de configuración

### `language`

- **Tipo:** `string`
- **Valores:** `"en"` (English), `"es"` (Español)
- **Default:** Detectado del sistema operativo (`navigator.language`)
- **Descripción:** Idioma de la interfaz de usuario.

### `theme`

- **Tipo:** `string`
- **Valores:** `"light"`, `"dark"`, `"system"`
- **Default:** `"system"`
- **Descripción:** Tema visual de la aplicación. `"system"` usa la preferencia del sistema operativo.

### `notifications`

- **Tipo:** `boolean`
- **Default:** `true`
- **Descripción:** Activa o desactiva las notificaciones del sistema (toast notifications).

### `start_minimized`

- **Tipo:** `boolean`
- **Default:** `false`
- **Descripción:** Si es `true`, la aplicación inicia minimizada en la bandeja del sistema.

### `tray_enabled`

- **Tipo:** `boolean`
- **Default:** `true`
- **Descripción:** Si es `true`, la aplicación se minimize a la bandeja del sistema al cerrar la ventana.

### `auto_start`

- **Tipo:** `boolean`
- **Default:** `false`
- **Descripción:** Si es `true`, la aplicación se ejecuta automáticamente al iniciar el sistema operativo. Utiliza el plugin de autostart de Tauri para registrar/desregistrar la app en el sistema.

### `refresh_rate`

- **Tipo:** `integer`
- **Rango:** 1 - 10
- **Default:** `2`
- **Unidad:** Segundos
- **Descripción:** Intervalo de actualización del dashboard y datos del sistema. Un valor más bajo提供 actualizaciones más frecuentes pero usa más CPU.

---

## Ejemplo de archivo de configuración

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

## Configuración por defecto

Si el archivo de configuración no existe o está dañado, se usa la configuración por defecto:

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

## Parámetros de compilación

### `Cargo.toml` (Backend)

| Campo | Valor |
|---|---|
| `name` | `energypy` |
| `version` | `2.0.1` |
| `description` | "Monitor de energía y sistema de escritorio multiplataforma" |
| `authors` | `["Rafael David Sanguino Ariza"]` |
| `edition` | `2021` |

### `tauri.conf.json`

| Campo | Valor |
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

| Campo | Valor |
|---|---|
| `name` | `energypy-v2` |
| `version` | `2.0.1` |
| `description` | "Monitor de energía y sistema de escritorio multiplataforma" |
| `svelte` | `^5.35.5` |
| `@tauri-apps/api` | `^2.8.0` |
| `@tauri-apps/plugin-autostart` | `^2.5.0` |
| `@tauri-apps/plugin-shell` | `^2.3.0` |
| `lucide-svelte` | `^0.544.0` |
| `tailwindcss` | `^4.1.13` |

---

## Logs

| Sistema | Ubicación |
|---|---|
| **Desarrollo** | `logs/energy_py.log` |
| **Producción** | Directorio de configuración del sistema |

### Nivel de log

- **Desarrollo:** `Debug` (todo incluido)
- **Producción:** `Info` (solo información y errores)

### Configurar nivel de log

```bash
# Debug verbose
RUST_LOG=debug npm run tauri dev

# Solo errores
RUST_LOG=error npm run tauri dev
```

---

## Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl+C` | Cancelar temporizador de energía en curso |
| `Ctrl+T` | Cambiar tema (claro / oscuro / sistema) |
| `Ctrl+Q` | Salir de la aplicación |

---

## Changelog

Consulta [CHANGELOG.md](../../CHANGELOG.md) para los cambios recientes.
