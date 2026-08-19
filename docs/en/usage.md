# EnergyPy — Usage

Complete guide to every application feature.

---

## Navigation

| Section | Access |
|---|---|
| **Dashboard** | "Dashboard" tab — Main panel with live metrics |
| **Processes** | "Processes" tab — System process manager |
| **Power** | "Power" tab — Power action control |
| **Settings** | "Settings" tab — Language, theme and options |
| **Minimize** | Title bar button — Minimizes to system tray |

---

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+C` | Cancel active power timer |
| `Ctrl+T` | Toggle theme (light / dark / system) |
| `Ctrl+Q` | Exit application |

---

## Dashboard

The monitoring panel displays real-time metrics:

| Card | Data shown |
|---|---|
| **CPU** | Overall usage, per-core, frequency, temperature (with color indicators), system uptime |
| **Memory** | RAM and swap: used, total, usage percentage |
| **Disk** | Reads/writes per second, used/free space |
| **Network** | Upload/download speed, active interfaces |
| **System Health** | Overall status progress bar |
| **Process List** | Top 5 processes by CPU usage — link to full manager |

### Skeleton loaders

While initial data is loading, each card displays an animated skeleton with a shimmer effect, indicating that information is being processed.

### Configurable refresh rate

The refresh interval is configured in **Settings > Refresh Rate**, with options from 1 to 10 seconds.

---

## Process Manager

Accessible from the "Processes" tab or the "View all" link on the dashboard.

### Features

- **Search** — Filter by process name, PID, or executable path.
- **Sorting** — Click any column header to sort.
- **Kill individual** — "Kill" button at the end of each row. Shows confirmation dialog.
- **Kill filtered** — "Kill Filtered" button to terminate all visible processes after a search.
- **Extended info** — Each row shows: name, PID, CPU usage, memory usage, full executable path, and uptime.
- **Scroll** — Table is fixed-height (max 500px) with internal scroll and sticky header.

### Supported processes

- Limit: 50 processes per query (sufficient for most common tasks).
- Information: PID, name, CPU usage (%), memory usage (%), executable path, time since start, bytes read/written.

---

## Power Control

### Schedule an action

1. Select the action: Shutdown, Restart, Suspend, Hibernate, or Lock.
2. Configure the timer: hours, minutes, seconds.
3. Press "Start". The progress bar shows remaining time.
4. You can cancel at any time with "Cancel" or `Ctrl+C`.

### Run now

Press "Run Now" to execute the action immediately. A confirmation dialog is shown before execution.

### Available actions

| Action | Description |
|---|---|
| **Shutdown** | Completely powers off the system |
| **Restart** | Restarts the system |
| **Suspend** | Sleep mode (low power) |
| **Hibernate** | Hibernate (no power, state saved to disk) |
| **Lock** | Locks the user session |

---

## Settings

| Option | Description |
|---|---|
| **Language** | Switch between Spanish and English |
| **Theme** | Light, Dark, or Follow System |
| **Notifications** | Enable/disable system notifications |
| **Auto-start** | Start EnergyPy when the computer boots |
| **Refresh Rate** | Dashboard refresh interval (1-10 seconds) |
| **About** | Developer information and GitHub profile link |

---

## Toast notifications

EnergyPy displays pop-up notifications for:

- Configuration save confirmations
- System operation errors
- Power action warnings
- Status change information

Notifications disappear automatically or can be closed manually.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Data not updating | Check the refresh interval in Settings |
| Process won't terminate | Some system processes require admin privileges |
| Temperature not displayed | Verify hardware sensors are available |
| Kill button missing | Verify the process is not a system process |

---

## Next step

- [Configuration](configuration.md) — Detailed configuration options reference.
