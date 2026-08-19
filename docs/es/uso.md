# EnergyPy — Uso

Guía completa de todas las funciones de la aplicación.

---

## Navegación

| Sección | Acceso |
|---|---|
| **Dashboard** | Pestaña "Dashboard" — Panel principal con métricas en vivo |
| **Procesos** | Pestaña "Procesos" — Gestor de procesos del sistema |
| **Energía** | Pestaña "Energía" — Control de acciones de energía |
| **Configuración** | Pestaña "Configuración" — Idioma, tema y opciones |
| **Minimizar** | Botón de la barra de título — Minimiza a la bandeja del sistema |

---

## Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl+C` | Cancelar temporizador de energía en curso |
| `Ctrl+T` | Cambiar tema (claro / oscuro / sistema) |
| `Ctrl+Q` | Salir de la aplicación |

---

## Dashboard

El panel de monitoreo muestra métricas en tiempo real:

| Tarjeta | Datos mostrados |
|---|---|
| **CPU** | Uso general, por núcleo, frecuencia, temperatura (con indicadores de color), uptime del sistema |
| **Memoria** | RAM y swap: usada, total, porcentaje de uso |
| **Disco** | Lecturas/escrituras por segundo, espacio usado/libre |
| **Red** | Velocidad de subida/bajada, interfaces activas |
| **Salud del sistema** | Barra de progreso del estado general |
| **Lista de procesos** | Top 5 procesos por uso de CPU — enlace al gestor completo |

### Skeleton loaders

Mientras se cargan los datos iniciales, cada tarjeta muestra un esqueleto animado con un efecto de brillo, indicando que la información está siendo procesada.

### Actualización configurable

El intervalo de refresco se configura en **Configuración > Actualización**, con opciones de 1 a 10 segundos.

---

## Gestor de procesos

Accesible desde la pestaña "Procesos" o desde el enlace "Ver todos" en el dashboard.

### Funciones

- **Búsqueda** — Filtra por nombre de proceso, PID o ruta del ejecutable.
- **Ordenación** — Haz clic en cualquier encabezado de columna para ordenar.
- **Mata individual** — Botón "Kill" al final de cada fila. Muestra diálogo de confirmación.
- **Mata filtrados** — Botón "Kill Filtered" para finalizar todos los procesos visibles tras una búsqueda.
- **Info extendida** — Cada fila muestra: nombre, PID, uso de CPU, uso de memoria, ruta completa del ejecutable y tiempo de actividad.
- **Scroll** — La tabla es fija en altura (máximo 500px) con scroll interno y encabezado pegajoso.

### Procesos soportados

- Límite: 50 procesos por consulta (suficiente para las tareas más comunes).
- Información: PID, nombre, uso de CPU (%), uso de memoria (%), ruta del ejecutable, tiempo desde inicio, bytes leídos/escritos.

---

## Control de Energía

### Programar una acción

1. Selecciona la acción: Apagar, Reiniciar, Suspender, Hibernar o Bloquear.
2. Configura el temporizador: horas, minutos, segundos.
3. Pulsa "Iniciar". La barra de progreso muestra el tiempo restante.
4. Puedes cancelar en cualquier momento con "Cancelar" o `Ctrl+C`.

### Ejecutar ahora

Pulsa "Ejecutar ahora" para ejecutar la acción inmediatamente. Se muestra un diálogo de confirmación antes de ejecutar.

### Acciones disponibles

| Acción | Descripción |
|---|---|
| **Apagar** | Apaga el sistema completamente |
| **Reiniciar** | Reinicia el sistema |
| **Suspender** | Suspender en modo sleep (bajo consumo) |
| **Hibernar** | Hibernar (sin consumo, estado guardado en disco) |
| **Bloquear** | Bloquea la sesión del usuario |

---

## Configuración

| Opción | Descripción |
|---|---|
| **Idioma** | Cambiar entre Español e Inglés |
| **Tema** | Claro, Oscuro o Seguir Sistema |
| **Notificaciones** | Activar/desactivar notificaciones del sistema |
| **Inicio automático** | Iniciar EnergyPy al encender el equipo |
| **Actualización** | Intervalo de refresco del dashboard (1-10 segundos) |
| **Autor** | Información del desarrollador y enlace al perfil de GitHub |

---

## Notificaciones toast

EnergyPy muestra notificaciones emergentes para:

- Confirmaciones de guardado de configuración
- Errores en operaciones del sistema
- Avisos de acciones de energía
- Información sobre cambios de estado

Las notificaciones desaparecen automáticamente o se pueden cerrar manualmente.

---

## Solución de problemas

| Problema | Solución |
|---|---|
| Datos no se actualizan | Verifica el intervalo de refresco en Configuración |
| Proceso no se puede finalizar | Algunos procesos del sistema requieren permisos de administrador |
| No se muestra temperatura | Verifica que los sensores de hardware estén disponibles |
| Botón kill no aparece | Verifica que el proceso no sea del sistema |

---

## Siguiente paso

- [Configuración](configuracion.md) — Referencia detallada de opciones de configuración.
