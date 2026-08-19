use serde::Serialize;
use std::collections::HashMap;
use std::process::{Command, Stdio};
use sysinfo::{CpuRefreshKind, Disks, Networks, System, MemoryRefreshKind, RefreshKind, Components};

fn run_silent_output(cmd: &str, args: &[&str]) -> Option<std::process::Output> {
    #[cfg(target_os = "windows")]
    {
        use std::os::windows::process::CommandExt;
        Command::new(cmd)
            .args(args)
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .creation_flags(0x08000000)
            .output()
            .ok()
    }
    #[cfg(not(target_os = "windows"))]
    {
        Command::new(cmd)
            .args(args)
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .output()
            .ok()
    }
}

#[derive(Debug, Serialize, Clone)]
pub struct CpuInfo {
    pub usage: f32,
    pub cores: Vec<f32>,
    pub frequency: u64,
    pub name: String,
    pub temperature: Option<f32>,
}

#[derive(Debug, Serialize, Clone)]
pub struct MemoryInfo {
    pub total: u64,
    pub used: u64,
    pub available: u64,
    pub percent: f32,
    pub swap_total: u64,
    pub swap_used: u64,
}

#[derive(Debug, Serialize, Clone)]
pub struct DiskInfo {
    pub name: String,
    pub mount_point: String,
    pub total: u64,
    pub used: u64,
    pub available: u64,
    pub percent: f32,
    pub file_system: String,
    pub is_removable: bool,
    pub is_read_only: bool,
}

#[derive(Debug, Serialize, Clone)]
pub struct NetworkInfo {
    pub interface: String,
    pub received: u64,
    pub transmitted: u64,
}

#[derive(Debug, Serialize, Clone)]
pub struct BatteryInfo {
    pub present: bool,
    pub percent: f32,
    pub charging: bool,
    pub time_to_full: Option<u64>,
    pub time_to_empty: Option<u64>,
}

#[derive(Debug, Serialize, Clone)]
pub struct ProcessInfo {
    pub pid: u32,
    pub name: String,
    pub cpu: f32,
    pub memory: u64,
    pub memory_percent: f32,
    pub exe: String,
    pub start_time: u64,
    pub disk_read: u64,
    pub disk_write: u64,
}

#[derive(Debug, Serialize, Clone)]
pub struct SystemStats {
    pub uptime_seconds: u64,
    pub hostname: String,
    pub os: String,
    pub kernel: String,
    pub arch: String,
    pub cpu: CpuInfo,
    pub memory: MemoryInfo,
    pub disks: Vec<DiskInfo>,
    pub networks: Vec<NetworkInfo>,
    pub battery: BatteryInfo,
    pub top_processes: Vec<ProcessInfo>,
}

pub struct SystemMonitor {
    system: System,
    disks: Disks,
    networks: Networks,
    components: Components,
    prev_net_rx: HashMap<String, u64>,
    prev_net_tx: HashMap<String, u64>,
}

impl SystemMonitor {
    pub fn kill_process(pid: u32) -> Result<(), String> {
        #[cfg(target_os = "windows")]
        {
            let output = std::process::Command::new("taskkill")
                .args(["/PID", &pid.to_string(), "/F"])
                .stdout(std::process::Stdio::piped())
                .stderr(std::process::Stdio::piped())
                .output()
                .map_err(|e| format!("Failed to run taskkill: {e}"))?;
            if output.status.success() {
                Ok(())
            } else {
                let stderr = String::from_utf8_lossy(&output.stderr);
                Err(format!("Failed to kill process {pid}: {stderr}"))
            }
        }
        #[cfg(target_os = "linux")]
        {
            unsafe {
                if libc::kill(pid as i32, libc::SIGKILL) == 0 {
                    Ok(())
                } else {
                    Err(format!("Failed to kill process {pid}: {}", std::io::Error::last_os_error()))
                }
            }
        }
        #[cfg(target_os = "macos")]
        {
            unsafe {
                if libc::kill(pid as i32, libc::SIGKILL) == 0 {
                    Ok(())
                } else {
                    Err(format!("Failed to kill process {pid}: {}", std::io::Error::last_os_error()))
                }
            }
        }
        #[cfg(not(any(target_os = "windows", target_os = "linux", target_os = "macos")))]
        {
            Err("Kill process not supported on this platform".to_string())
        }
    }

    pub fn new() -> Self {
        let mut system = System::new_with_specifics(
            RefreshKind::nothing()
                .with_cpu(CpuRefreshKind::everything())
                .with_memory(MemoryRefreshKind::everything()),
        );
        system.refresh_cpu_all();
        system.refresh_memory();

        let disks = Disks::new_with_refreshed_list();
        let networks = Networks::new_with_refreshed_list();
        let components = Components::new_with_refreshed_list();

        let mut prev_net_rx = HashMap::new();
        let mut prev_net_tx = HashMap::new();
        for (name, data) in &networks {
            prev_net_rx.insert(name.clone(), data.total_received());
            prev_net_tx.insert(name.clone(), data.total_transmitted());
        }

        Self {
            system,
            disks,
            networks,
            components,
            prev_net_rx,
            prev_net_tx,
        }
    }

    pub fn refresh(&mut self) {
        self.system.refresh_cpu_all();
        self.system.refresh_memory();
        self.system.refresh_processes(sysinfo::ProcessesToUpdate::All, true);
        self.disks.refresh(false);
        self.components.refresh(true);

        self.prev_net_rx.clear();
        self.prev_net_tx.clear();
        for (name, data) in &self.networks {
            self.prev_net_rx.insert(name.clone(), data.total_received());
            self.prev_net_tx.insert(name.clone(), data.total_transmitted());
        }
        self.networks.refresh(true);
    }

    pub fn get_stats(&mut self) -> SystemStats {
        self.refresh();

        let cpu_temp = self.components.iter()
            .find(|c| {
                let label = c.label().to_lowercase();
                label.contains("cpu") || label.contains("processor") || label.contains("core")
            })
            .map(|c| c.temperature())
            .flatten()
            .or_else(|| {
                self.components.iter()
                    .find(|c| c.temperature().is_some())
                    .and_then(|c| c.temperature())
            });

        let cpu = CpuInfo {
            usage: self.system.global_cpu_usage(),
            cores: self.system.cpus().iter().map(|c| c.cpu_usage()).collect(),
            frequency: self.system.cpus().first().map(|c| c.frequency()).unwrap_or(0),
            name: self
                .system
                .cpus()
                .first()
                .map(|c| c.brand().to_string())
                .unwrap_or_default(),
            temperature: cpu_temp,
        };

        let memory = MemoryInfo {
            total: self.system.total_memory(),
            used: self.system.used_memory(),
            available: self.system.available_memory(),
            percent: if self.system.total_memory() > 0 {
                (self.system.used_memory() as f32 / self.system.total_memory() as f32) * 100.0
            } else {
                0.0
            },
            swap_total: self.system.total_swap(),
            swap_used: self.system.used_swap(),
        };

        let prev_rx = &self.prev_net_rx;
        let prev_tx = &self.prev_net_tx;

        let networks: Vec<NetworkInfo> = self
            .networks
            .iter()
            .map(|(name, data)| {
                let old_rx = prev_rx.get(name).copied().unwrap_or(0);
                let old_tx = prev_tx.get(name).copied().unwrap_or(0);
                NetworkInfo {
                    interface: name.clone(),
                    received: data.total_received().saturating_sub(old_rx),
                    transmitted: data.total_transmitted().saturating_sub(old_tx),
                }
            })
            .collect();

        let disks: Vec<DiskInfo> = self
            .disks
            .iter()
            .map(|d| {
                let total = d.total_space();
                let available = d.available_space();
                DiskInfo {
                    name: d.name().to_string_lossy().to_string(),
                    mount_point: d.mount_point().to_string_lossy().to_string(),
                    total,
                    used: total.saturating_sub(available),
                    available,
                    percent: if total > 0 {
                        (total.saturating_sub(available)) as f32 / total as f32 * 100.0
                    } else {
                        0.0
                    },
                    file_system: d.file_system().to_string_lossy().to_string(),
                    is_removable: d.is_removable(),
                    is_read_only: d.is_read_only(),
                }
            })
            .collect();

        let battery = Self::get_battery_info();

        let mut top_processes: Vec<ProcessInfo> = self
            .system
            .processes()
            .iter()
            .map(|(pid, p)| {
                let disk_usage = p.disk_usage();
                ProcessInfo {
                    pid: pid.as_u32(),
                    name: p.name().to_string_lossy().to_string(),
                    cpu: p.cpu_usage(),
                    memory: p.memory(),
                    memory_percent: if self.system.total_memory() > 0 {
                        (p.memory() as f32 / self.system.total_memory() as f32) * 100.0
                    } else {
                        0.0
                    },
                    exe: p.exe().map(|e| e.to_string_lossy().to_string()).unwrap_or_default(),
                    start_time: p.start_time(),
                    disk_read: disk_usage.read_bytes,
                    disk_write: disk_usage.written_bytes,
                }
            })
            .filter(|p| p.cpu > 0.0 || p.memory_percent > 0.0)
            .collect();

        top_processes.sort_by(|a, b| b.cpu.partial_cmp(&a.cpu).unwrap_or(std::cmp::Ordering::Equal));
        top_processes.truncate(50);

        SystemStats {
            uptime_seconds: System::uptime(),
            hostname: System::host_name().unwrap_or_default(),
            os: System::long_os_version().unwrap_or_default(),
            kernel: System::kernel_version().unwrap_or_default(),
            arch: std::env::consts::ARCH.to_string(),
            cpu,
            memory,
            disks,
            networks,
            battery,
            top_processes,
        }
    }

    fn get_battery_info() -> BatteryInfo {
        #[cfg(target_os = "windows")]
        {
            let output = run_silent_output("powershell", &[
                "-NoProfile",
                "-Command",
                "Get-CimInstance -ClassName Win32_Battery | Select-Object EstimatedChargeRemaining,BatteryStatus,EstimatedRunTime | ConvertTo-Json -Compress",
            ]);

            if let Some(output) = output {
                let stdout = String::from_utf8_lossy(&output.stdout);
                let trimmed = stdout.trim();
                if !trimmed.is_empty() {
                    if let Ok(value) = serde_json::from_str::<serde_json::Value>(trimmed) {
                        let batteries = match value {
                            serde_json::Value::Array(items) => items,
                            serde_json::Value::Object(_) => vec![value],
                            _ => Vec::new(),
                        };
                        if let Some(batt) = batteries.first() {
                            let percent = batt
                                .get("EstimatedChargeRemaining")
                                .and_then(|v| v.as_f64())
                                .unwrap_or(0.0) as f32;
                            let status = batt
                                .get("BatteryStatus")
                                .and_then(|v| v.as_u64())
                                .unwrap_or(1);
                            let charging = status == 2 || status == 6;
                            let runtime_minutes = batt
                                .get("EstimatedRunTime")
                                .and_then(|v| v.as_u64())
                                .filter(|&m| m != u32::MAX as u64)
                                .unwrap_or(0);
                            let runtime_seconds = runtime_minutes.saturating_mul(60);

                            return BatteryInfo {
                                present: true,
                                percent,
                                charging,
                                time_to_full: if charging && runtime_seconds > 0 { Some(runtime_seconds) } else { None },
                                time_to_empty: if !charging && runtime_seconds > 0 { Some(runtime_seconds) } else { None },
                            };
                        }
                    }
                }
            }
            BatteryInfo { present: false, percent: 0.0, charging: false, time_to_full: None, time_to_empty: None }
        }

        #[cfg(target_os = "linux")]
        {
            let entries = std::fs::read_dir("/sys/class/power_supply").ok();
            if let Some(entries) = entries {
                let mut percent = 0.0f32;
                let mut charging = false;
                let mut found = false;
                for entry in entries.flatten() {
                    let name = entry.file_name().to_string_lossy().to_string();
                    if !(name.starts_with("BAT") || name.starts_with("battery")) {
                        continue;
                    }
                    let uevent = std::fs::read_to_string(entry.path().join("uevent")).unwrap_or_default();
                    for line in uevent.lines() {
                        if let Some(val) = line.strip_prefix("POWER_SUPPLY_CAPACITY=") {
                            percent = val.trim().parse::<f32>().unwrap_or(0.0);
                            found = true;
                        } else if let Some(val) = line.strip_prefix("POWER_SUPPLY_STATUS=") {
                            charging = val.trim() == "Charging";
                        }
                    }
                }
                if found {
                    return BatteryInfo {
                        present: found,
                        percent,
                        charging,
                        time_to_full: None,
                        time_to_empty: None,
                    };
                }
            }
            BatteryInfo { present: false, percent: 0.0, charging: false, time_to_full: None, time_to_empty: None }
        }

        #[cfg(target_os = "macos")]
        {
            let output = run_silent_output("pmset", &["-g", "batt"]);
            if let Some(output) = output {
                let stdout = String::from_utf8_lossy(&output.stdout);
                if let Some(line) = stdout.lines().nth(1) {
                    let parts: Vec<&str> = line.split(';').collect();
                    let percent = parts.first()
                        .and_then(|p| p.trim().split_whitespace().last())
                        .and_then(|p| p.trim_end_matches('%').parse::<f32>().ok())
                        .unwrap_or(0.0);
                    let charging = parts.get(1).map(|s| s.trim() == "charging").unwrap_or(false);
                    let time_str = parts.get(2).map(|s| s.trim()).unwrap_or("");
                    let time_seconds = if time_str.contains(":") {
                        let t: Vec<&str> = time_str.split(':').collect();
                        let h: u64 = t.first().and_then(|s| s.parse().ok()).unwrap_or(0);
                        let m: u64 = t.get(1).and_then(|s| s.parse().ok()).unwrap_or(0);
                        Some((h * 60 + m) * 60)
                    } else {
                        None
                    };
                    return BatteryInfo {
                        present: true,
                        percent,
                        charging,
                        time_to_full: if charging { time_seconds } else { None },
                        time_to_empty: if !charging { time_seconds } else { None },
                    };
                }
            }
            BatteryInfo { present: false, percent: 0.0, charging: false, time_to_full: None, time_to_empty: None }
        }

        #[cfg(not(any(target_os = "windows", target_os = "linux", target_os = "macos")))]
        {
            BatteryInfo { present: false, percent: 0.0, charging: false, time_to_full: None, time_to_empty: None }
        }
    }
}
