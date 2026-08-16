# 🛠️ Guía de Instalación — EnergyPy

> **Índice de docs:** [README](../README.md) · [Uso](uso.md) · [Desarrollo](desarrollo.md) · [Arquitectura](arquitectura.md) · [Configuración](configuracion.md)

---

## Requisitos del sistema

| Sistema Operativo | Requisitos mínimos |
|---|---|
| **Windows** | Windows 10/11 (64-bit) |
| **macOS** | macOS 10.15+ (Catalina o superior) |
| **Linux** | WebKitGTK 4.1, GTK 3 (distros basadas en Debian/Ubuntu, Fedora, Arch) |

**Recursos:** ~30 MB de espacio en disco · 128 MB de RAM · cualquier CPU compatible con 64-bit.

---

## Windows

### Opción 1: Instalador MSI (recomendado)
1. Descarga `EnergyPy_2.0.0_x64_en-US.msi` desde los Releases.
2. Doble clic en el archivo y sigue el asistente.
3. EnergyPy aparecerá en el menú Inicio y en el Escritorio.

### Opción 2: Instalador NSIS
1. Descarga `EnergyPy_2.0.0_x64-setup.exe`.
2. Ejecuta el instalador. Tendrás opciones de instalación por usuario o por sistema, y personalización de carpeta.

### Opción 3: Portátil (sin instalación)
1. Descarga el ejecutable `energypy_v20.exe`.
2. Cópialo a la carpeta que prefieras (por ejemplo, una unidad USB).
3. Ejecútalo directamente. No requiere permisos de administrador para ejecutarse (algunas acciones de energía podrían requerirlos).

---

## macOS

1. Descarga el paquete `.dmg` desde los Releases.
2. Abre el archivo `.dmg` y arrastra EnergyPy a la carpeta **Aplicaciones**.
3. Abre EnergyPy desde Launchpad o la carpeta Aplicaciones.
4. Si macOS muestra una advertencia de "desarrollador no verificado", ve a **Preferencias del Sistema → Privacidad y seguridad** y haz clic en **Abrir de todos modos**.

---

## Linux

### Debian / Ubuntu (`.deb`)
```bash
sudo dpkg -i EnergyPy_2.0.0_amd64.deb
sudo apt-get install -f   # desinstala dependencias faltantes si las hay
```

### AppImage
```bash
chmod +x EnergyPy_2.0.0.AppImage
./EnergyPy_2.0.0.AppImage
```

### Dependencias necesarias (Debian/Ubuntu)
```bash
sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf
```

---

## Verificación de la instalación

1. Abre EnergyPy.
2. Deberías ver el **Dashboard** con las estadísticas en vivo de tu sistema.
3. Ve a **Configuración** y cambia el tema a oscuro como prueba.
4. Cierra la ventana — debería minimizarse a la bandeja del sistema (si está habilitado).

---

## Solución de problemas

| Problema | Solución |
|---|---|
| Reactivos acciones de energía requieren administrador | Ejecuta la app como administrador en Windows (clic derecho → "Ejecutar como administrador") |
| La batería no se detecta en Linux | Verifica que exista `/sys/class/power_supply/BAT0` o `BAT1` |
| No aparece la bandeja en Linux | Instala el paquete de indicadores de tu distribución (ej. `libayatana-appindicator`) |
| La consola parpadea en Windows | Ya corregido en v2.0.0 — usa la última versión |

---

[← Índice](../README.md) · [Siguiente: Guía de Uso →](uso.md)