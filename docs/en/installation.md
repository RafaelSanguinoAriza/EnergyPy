# 🛠️ Installation Guide — EnergyPy

> **Docs index:** [README](../README.md) · [Usage](usage.md) · [Development](development.md) · [Architecture](architecture.md) · [Configuration](configuration.md)

---

## System requirements

| Operating System | Minimum requirements |
|---|---|
| **Windows** | Windows 10/11 (64-bit) |
| **macOS** | macOS 10.15+ (Catalina or later) |
| **Linux** | WebKitGTK 4.1, GTK 3 (Debian/Ubuntu-based, Fedora, Arch) |

**Resources:** ~30 MB disk space · 128 MB RAM · any 64-bit capable CPU.

---

## Windows

### Option 1: MSI installer (recommended)
1. Download `EnergyPy_2.0.0_x64_en-US.msi` from Releases.
2. Double-click the file and follow the wizard.
3. EnergyPy will appear in the Start Menu and Desktop.

### Option 2: NSIS installer
1. Download `EnergyPy_2.0.0_x64-setup.exe`.
2. Run the installer. You get per-user or per-machine install options and custom folder selection.

### Option 3: Portable (no install)
1. Download the `energypy_v20.exe` executable.
2. Copy it to your preferred folder (e.g. a USB drive).
3. Run it directly. No administrator rights needed to run (some power actions may require them).

---

## macOS

1. Download the `.dmg` package from Releases.
2. Open the `.dmg` and drag EnergyPy to **Applications**.
3. Open EnergyPy from Launchpad or the Applications folder.
4. If macOS shows an "unidentified developer" warning, go to **System Preferences → Privacy & Security** and click **Open Anyway**.

---

## Linux

### Debian / Ubuntu (`.deb`)
```bash
sudo dpkg -i EnergyPy_2.0.0_amd64.deb
sudo apt-get install -f   # install missing dependencies if any
```

### AppImage
```bash
chmod +x EnergyPy_2.0.0.AppImage
./EnergyPy_2.0.0.AppImage
```

### Required dependencies (Debian/Ubuntu)
```bash
sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf
```

---

## Verifying the installation

1. Open EnergyPy.
2. You should see the **Dashboard** with live system statistics.
3. Go to **Settings** and switch the theme to dark as a test.
4. Close the window — it should minimize to the system tray (if enabled).

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Some power actions require admin rights | Run the app as administrator on Windows (right-click → "Run as administrator") |
| Battery not detected on Linux | Verify `/sys/class/power_supply/BAT0` or `BAT1` exists |
| No tray icon on Linux | Install your distribution's indicator package (e.g. `libayatana-appindicator`) |
| Console flashes on Windows | Fixed in v2.0.0 — use the latest version |

---

[← Index](../README.md) · [Next: Usage Guide →](usage.md)