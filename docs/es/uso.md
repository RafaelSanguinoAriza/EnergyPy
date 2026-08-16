# 🚀 Guía de Uso — EnergyPy

> **Índice de docs:** [README](../README.md) · [Instalación](instalacion.md) · [Desarrollo](desarrollo.md) · [Arquitectura](arquitectura.md) · [Configuración](configuracion.md)

---

## Navegación

La aplicación tiene una barra lateral con tres secciones:

- **Dashboard** — Monitoreo del sistema en tiempo real
- **Control de Energía** — Programación de acciones de energía
- **Configuración** — Preferencias de la aplicación

En ventanas pequeñas, la barra lateral se colapsa mostrando solo iconos.

---

## 📊 Dashboard

El dashboard muestra tarjetas con estadísticas que se actualizan automáticamente cada **2 segundos**.

### CPU
- **Uso total** — porcentaje global del procesador con barra de progreso.
- **Por núcleo** — barras individuales de cada núcleo (C0, C1, ...).
- **Frecuencia** — frecuencia actual en GHz/MHz.
- **Nombre** — modelo del procesador.

> Los colores indican carga: verde (< 50%), amarillo (50–80%), rojo (> 80%).

### Memoria (RAM)
- Uso total con barra de progreso.
- **Total / Usado / Disponible** en formato legible (GB).
- **Swap** — información de memoria de intercambio si existe.

### Disco
- Una barra por partición/unidad montada.
- **Usado / Total** y **espacio libre**.
- Umbrales de color: rojo > 85%, amarillo > 60%.

### Red
- Velocidad de **descarga (↓)** y **subida (↑)** por interfaz en bps/Kbps/Mbps/Gbps.
- Se muestra el tráfico diferencial entre mediciones (velocidad, no totales).

### Tiempo de actividad
- Duración desde el último arranque del sistema (días, horas, minutos).
- **Hostname** y **sistema operativo**.

### Batería
- Porcentaje de carga con icono dinámico (cargando/descargando).
- Tiempo estimado de carga completa o de duración restante.
- En equipos sin batería, muestra "Sin batería detectada".

### Procesos principales
- Los 10 procesos con mayor uso de CPU.
- Muestra PID, nombre, uso de CPU % y uso de memoria.

---

## ⏰ Control de Energía

### Programar una acción

1. Ve a la sección **Control de Energía**.
2. Selecciona el tipo de acción: **Apagar**, **Reiniciar**, **Suspender**, **Hibernar** o **Bloquear**.
3. Elige el método de programación:

| Método | Descripción |
|---|---|
| **Programar por tiempo** | Introduce una cantidad y elige la unidad (segundos, minutos, horas) |
| **Programar a hora exacta** | Selecciona la hora del día en que se ejecutará la acción |

4. Haz clic en el botón de programar.
5. Confirma la acción en el diálogo de advertencia.
6. Verás el **conteo regresivo** con barra de progreso y animación.

> ⚠️ **Nota sobre horas exactas:** si la hora ya pasó, la acción se programa para el día siguiente.

### Cancelar una acción

- Haz clic en **Cancelar** durante el conteo regresivo, **o**
- Pulsa **Ctrl+C** en cualquier momento.

> ✅ Al cancelar, la acción programada se aborta completamente (el sistema verifica que el comando original no se ejecute).

### Comportamiento al completarse

Cuando el conteo llega a cero, la acción se ejecuta:
- **Windows**: `shutdown /s /r /h`, `rundll32` para suspender/bloquear.
- **Linux**: `shutdown`, `systemctl`, `loginctl`.
- **macOS**: `shutdown`, `pmset`.

Algunas acciones (suspender/hibernar) pueden requerir permisos de administrador en ciertos sistemas.

---

## ⚙️ Configuración

### Idioma
- Cambia entre **Español** e **English** al instante. Todo el interfaz se actualiza al momento.

### Apariencia
- **Tema**: Claro, Oscuro o Sistema (sigue al sistema operativo).
- Atajo: **Ctrl+T** para alternar.

### General
- **Notificaciones** — habilita/deshabilita avisos del sistema.
- **Minimizar a bandeja** — al cerrar la ventana, se oculta a la bandeja en lugar de salir.
- **Iniciar minimizado** — la app arranca oculta en la bandeja.
- **Actualización automática** — busca e instala nuevas versiones automáticamente.

### Guardar cambios
- **Guardar ajustes** — persiste la configuración en disco.
- **Restablecer valores** — vuelve a los valores predeterminados.

---

## ⌨️ Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl + C` | Cancelar acción de energía programada |
| `Ctrl + T` | Alternar tema (claro → oscuro → sistema) |
| `Ctrl + Q` | Salir de la aplicación |

> En macOS, usa `Cmd` en lugar de `Ctrl`.

---

## 🗔 Bandeja del sistema

- Al cerrar la ventana, la app **se minimiza a la bandeja** (si está habilitado).
- Icono de bandeja con menú contextual: **Mostrar EnergyPy** y **Salir**.
- Clic en el icono de bandeja restaura la ventana principal.

---

[← Instalación](instalacion.md) · [Siguiente: Desarrollo →](desarrollo.md)