# EnergyPy — Installation

Installation guide for Windows, Linux, and macOS.

---

## Prerequisites

| Component | Windows | Linux | macOS |
|---|---|---|---|
| OS | Windows 10/11 (64-bit) | Ubuntu 22.04+ / Fedora 38+ | macOS 13 Ventura+ |
| Runtime | WebView2 (included in updated Win 10/11) | libwebkit2gtk | WebKit (included in macOS) |
| RAM | 256 MB free | 256 MB free | 256 MB free |
| Disk | ~22 MB | ~22 MB | ~22 MB |

---

## Windows

### NSIS Installer (recommended)

1. Download `EnergyPy_2.0.1_x64-setup.exe` from [GitHub Releases](https://github.com/RafaelSanguinoAriza/EnergyPy/releases).
2. Run the installer. No admin rights required.
3. The app installs to `C:\Users\<your_user>\AppData\Local\EnergyPy\`.

### MSI Installer

1. Download `EnergyPy_2.0.1_x64_en-US.msi` from [GitHub Releases](https://github.com/RafaelSanguinoAriza/EnergyPy/releases).
2. Run the MSI. May require admin rights depending on your configuration.

### Portable version

1. Download `EnergyPy_2.0.1_x64_portable.zip`.
2. Extract the zip to any folder.
3. Run `energypy_v20.exe` directly.
4. **Important:** `WebView2Loader.dll` must remain next to the `.exe`.

> If Windows SmartScreen shows a warning, click "More info" and then "Run anyway".

---

## Linux

> **Status:** Coming soon. Linux builds will be available when the D-Bus power daemon implementation is complete.

### Requirements (coming soon)

```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev

# Fedora
sudo dnf install webkit2gtk4.1-devel libappindicator-gtk3-devel librsvg2-devel
```

---

## macOS

> **Status:** Coming soon. macOS builds will be available after validating the `pmset` and `launchd` integration.

### Requirements (coming soon)

```bash
# Homebrew
brew install curl wget
```

---

## Verifying the installation

1. Open EnergyPy from the Start menu, launcher, or terminal.
2. Navigate through the tabs: Dashboard, Processes, Power, Settings.
3. Verify that system data updates correctly.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| EnergyPy won't start on Windows | Verify WebView2 is installed: [Download WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) |
| Blank screen on startup | Update your graphics drivers |
| High CPU on Linux | Verify the power daemon is available |
| CPU temperature not showing | Some sensors require root permissions on Linux |

---

## Next step

- [Application usage](usage.md) — Complete guide to every feature.
