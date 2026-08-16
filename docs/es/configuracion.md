# ⚙️ Configuración — EnergyPy

> **Índice de docs:** [README](../README.md) · [Instalación](instalacion.md) · [Uso](uso.md) · [Desarrollo](desarrollo.md) · [Arquitectura](arquitectura.md)

---

## Archivo de configuración

EnergyPy guarda sus preferencias en un archivo JSON. Ubicación según el sistema:

| Sistema | Ruta |
|---|---|
| **Windows** | `%APPDATA%\EnergyPy\config.json` |
| **Linux** | `~/.config/EnergyPy/config.json` |
| **macOS** | `~/Library/Application Support/EnergyPy/config.json` |

La configuración se carga automáticamente al iniciar la aplicación y se guarda al pulsar **"Guardar ajustes"** en la sección de Configuración.

---

## Opciones

### `theme`
Tema de la interfaz.

| Valor | Efecto |
|---|---|
| `"light"` | Tema claro |
| `"dark"` | Tema oscuro |
| `"system"` | Sigue al sistema operativo (por defecto) |

### `language`
Idioma de la interfaz.

| Valor | Efecto |
|---|---|
| `"en"` | Inglés |
| `"es"` | Español |

### `notifications_enabled`
Booleano. Habilita/deshabilita las notificaciones del sistema.

### `minimize_to_tray`
Booleano. Cuando `true`, al cerrar la ventana la app se oculta en la bandeja en lugar de salir.

### `start_minimized`
Booleano. Cuando `true`, la app arranca oculta en la bandeja.

### `auto_update`
Booleano. Cuando `true`, la app comprueba y aplica actualizaciones automáticamente.

### `last_tab`
Cadena. Última sección visitada (`"dashboard"`, `"power"`, `"settings"`).

---

## Ejemplo de archivo

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

## Archivo de logs

El registro de actividad (`energypy.log`) se encuentra en el mismo directorio que `config.json`:

| Sistema | Ruta |
|---|---|
| **Windows** | `%APPDATA%\EnergyPy\energypy.log` |
| **Linux** | `~/.config/EnergyPy/energypy.log` |
| **macOS** | `~/Library/Application Support/EnergyPy/energypy.log` |

---

## Configuración del empaquetado (`tauri.conf.json`)

Archivo en `src-tauri/tauri.conf.json`:

| Clave | Descripción |
|---|---|
| `productName` | Nombre del producto (`EnergyPy`) |
| `version` | Versión de la app (`2.0.0`) |
| `identifier` | Identificador único (`com.energypy.desktop`) |
| `app.windows` | Configuración de ventana (tamaño, título, centrado) |
| `bundle.icon` | Iconos de cada plataforma |
| `plugins.updater` | Endpoint de actualizaciones y clave pública |

---

## Permisos (`capabilities/default.json`)

Define los permisos de la app para cada plugin de Tauri:

- **opener**: abrir URLs en el navegador externo.
- **notification**: enviar notificaciones.
- **shell**: ejecutar comandos/abrir archivos.
- **autostart**: iniciar con el sistema.
- **process**: salir / reiniciar el proceso.
- **dialog**: diálogos nativos (confirmación).
- **updater**: comprobar y descargar actualizaciones.
- **core:event**: suscribirse a eventos (stats, countdown).

---

[← Arquitectura](arquitectura.md) · [Volver al índice](../README.md)