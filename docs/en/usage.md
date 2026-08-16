# 🚀 Usage Guide — EnergyPy

> **Docs index:** [README](../README.md) · [Installation](installation.md) · [Development](development.md) · [Architecture](architecture.md) · [Configuration](configuration.md)

---

## Navigation

The app has a sidebar with three sections:

- **Dashboard** — Real-time system monitoring
- **Power Control** — Scheduling power actions
- **Settings** — Application preferences

On narrow windows the sidebar collapses to icons only.

---

## 📊 Dashboard

The dashboard shows cards with statistics that auto-refresh every **2 seconds**.

### CPU
- **Total usage** — overall processor percentage with a progress bar.
- **Per-core** — individual bars for each core (C0, C1, ...).
- **Frequency** — current frequency in GHz/MHz.
- **Name** — processor model.

> Colors indicate load: green (< 50%), yellow (50–80%), red (> 80%).

### Memory (RAM)
- Total usage with progress bar.
- **Total / Used / Available** in a human-readable format (GB).
- **Swap** — swap information when present.

### Disk
- One bar per partition/mounted drive.
- **Used / Total** and **free space**.
- Color thresholds: red > 85%, yellow > 60%.

### Network
- **Download (↓)** and **upload (↑)** speed per interface in bps/Kbps/Mbps/Gbps.
- Shows the differential traffic between measurements (speed, not totals).

### Uptime
- Time since the last system boot (days, hours, minutes).
- **Hostname** and **operating system**.

### Battery
- Charge percentage with a dynamic icon (charging/discharging).
- Estimated time to full or remaining time.
- On machines without a battery, shows "No battery detected".

### Top processes
- The 10 processes with the highest CPU usage.
- Shows PID, name, CPU % and memory usage.

---

## ⏰ Power Control

### Scheduling an action

1. Go to the **Power Control** section.
2. Select the action type: **Shutdown**, **Restart**, **Suspend**, **Hibernate** or **Lock**.
3. Choose the scheduling method:

| Method | Description |
|---|---|
| **Schedule by time** | Enter an amount and pick the unit (seconds, minutes, hours) |
| **Schedule at exact hour** | Pick the time of day when the action will run |

4. Click the schedule button.
5. Confirm the action in the warning dialog.
6. You'll see the **countdown** with a progress bar and animation.

> ⚠️ **Note on exact hours:** if the time has already passed, the action is scheduled for the next day.

### Cancelling an action

- Click **Cancel** during the countdown, **or**
- Press **Ctrl+C** at any time.

> ✅ Cancelling fully aborts the scheduled action (the system verifies the original command never executes).

### Behaviour on completion

When the countdown reaches zero, the action runs:
- **Windows**: `shutdown /s /r /h`, `rundll32` for suspend/lock.
- **Linux**: `shutdown`, `systemctl`, `loginctl`.
- **macOS**: `shutdown`, `pmset`.

Some actions (suspend/hibernate) may require administrator rights on certain systems.

---

## ⚙️ Settings

### Language
- Switch between **English** and **Español** instantly. The whole UI updates at once.

### Appearance
- **Theme**: Light, Dark or System (follows the OS).
- Shortcut: **Ctrl+T** to cycle.

### General
- **Notifications** — enable/disable system alerts.
- **Minimize to tray** — closing the window hides it to the tray instead of exiting.
- **Start minimized** — the app starts hidden in the tray.
- **Auto update** — automatically checks and installs new versions.

### Saving changes
- **Save settings** — persists the configuration to disk.
- **Reset to defaults** — restores the default values.

---

## ⌨️ Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + C` | Cancel the scheduled power action |
| `Ctrl + T` | Toggle theme (light → dark → system) |
| `Ctrl + Q` | Quit the application |

> On macOS, use `Cmd` instead of `Ctrl`.

---

## 🗔 System tray

- Closing the window **minimizes to the tray** (if enabled).
- Tray icon with a context menu: **Show EnergyPy** and **Quit**.
- Clicking the tray icon restores the main window.

---

[← Installation](installation.md) · [Next: Development →](development.md)