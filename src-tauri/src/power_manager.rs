use chrono::{Local, NaiveTime, Timelike};
use serde::{Deserialize, Serialize};
use std::process::{Command, Stdio};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Instant;
use tauri::{AppHandle, Emitter};

fn run_command(cmd: &str, args: &[&str]) -> Result<(), String> {
    #[cfg(target_os = "windows")]
    {
        use std::os::windows::process::CommandExt;
        let status = Command::new(cmd)
            .args(args)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .creation_flags(0x08000000)
            .status()
            .map_err(|e| format!("Failed to execute {cmd}: {e}"))?;
        if status.success() {
            Ok(())
        } else {
            Err(format!("Command {cmd} failed with code {:?}", status.code()))
        }
    }
    #[cfg(not(target_os = "windows"))]
    {
        let status = Command::new(cmd)
            .args(args)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status()
            .map_err(|e| format!("Failed to execute {cmd}: {e}"))?;
        if status.success() {
            Ok(())
        } else {
            Err(format!("Command {cmd} failed with code {:?}", status.code()))
        }
    }
}

fn run_command_with_output(cmd: &str, args: &[&str]) -> Option<std::process::Output> {
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

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ActionType {
    Shutdown,
    Restart,
    Suspend,
    Hibernate,
    Lock,
}

impl ActionType {
    pub fn label(&self) -> &'static str {
        match self {
            ActionType::Shutdown => "Shutdown",
            ActionType::Restart => "Restart",
            ActionType::Suspend => "Suspend",
            ActionType::Hibernate => "Hibernate",
            ActionType::Lock => "Lock",
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct ScheduledAction {
    pub action_type: ActionType,
    pub total_seconds: u64,
    pub remaining_seconds: u64,
    pub active: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ActionResult {
    pub success: bool,
    pub message: String,
    pub action_type: String,
}

pub struct PowerManager {
    scheduled: Arc<Mutex<Option<ScheduledActionInner>>>,
    generation: Arc<AtomicU64>,
}

struct ScheduledActionInner {
    action_type: ActionType,
    total_seconds: u64,
    start_time: Instant,
}

impl PowerManager {
    pub fn new() -> Self {
        Self {
            scheduled: Arc::new(Mutex::new(None)),
            generation: Arc::new(AtomicU64::new(0)),
        }
    }

    pub fn schedule(&self, seconds: u64, action_type: ActionType, app: AppHandle) {
        let generation = self.generation.fetch_add(1, Ordering::SeqCst) + 1;
        let inner = ScheduledActionInner {
            action_type: action_type.clone(),
            total_seconds: seconds,
            start_time: Instant::now(),
        };
        *self.scheduled.lock().unwrap() = Some(inner);

        let action = action_type.clone();
        let current_generation = Arc::clone(&self.generation);
        let scheduled = Arc::clone(&self.scheduled);
        std::thread::spawn(move || {
            std::thread::sleep(std::time::Duration::from_secs(seconds));
            if current_generation.load(Ordering::SeqCst) == generation {
                let label = action.label();
                let result = execute_action(&action);
                match result {
                    Ok(()) => {
                        let _ = app.emit(
                            "power-action-result",
                            &ActionResult {
                                success: true,
                                message: format!("Action {label} executed"),
                                action_type: label.to_string(),
                            },
                        );
                    }
                    Err(e) => {
                        let _ = app.emit(
                            "power-action-result",
                            &ActionResult {
                                success: false,
                                message: e,
                                action_type: label.to_string(),
                            },
                        );
                    }
                }
                if current_generation.load(Ordering::SeqCst) == generation {
                    *scheduled.lock().unwrap() = None;
                }
            }
        });
    }

    pub fn schedule_at_time(&self, action_type: ActionType, target_time: NaiveTime, app: AppHandle) -> Result<u64, String> {
        let now = Local::now().time();
        let diff = seconds_until(target_time, now);
        self.schedule(diff, action_type, app);
        Ok(diff)
    }

    pub fn cancel(&self) -> bool {
        let mut scheduled = self.scheduled.lock().unwrap();
        if scheduled.is_some() {
            *scheduled = None;
            self.generation.fetch_add(1, Ordering::SeqCst);
            #[cfg(target_os = "windows")]
            { let _ = run_command("shutdown", &["/a"]); }
            #[cfg(any(target_os = "linux", target_os = "macos"))]
            { let _ = run_command("shutdown", &["-c"]); }
            true
        } else {
            false
        }
    }

    pub fn get_scheduled(&self) -> ScheduledAction {
        let scheduled = self.scheduled.lock().unwrap();
        match scheduled.as_ref() {
            Some(inner) => {
                let elapsed = inner.start_time.elapsed().as_secs();
                let remaining = inner.total_seconds.saturating_sub(elapsed);
                ScheduledAction {
                    action_type: inner.action_type.clone(),
                    total_seconds: inner.total_seconds,
                    remaining_seconds: remaining,
                    active: remaining > 0,
                }
            }
            None => ScheduledAction {
                action_type: ActionType::Shutdown,
                total_seconds: 0,
                remaining_seconds: 0,
                active: false,
            },
        }
    }

    pub fn is_admin() -> bool {
        #[cfg(target_os = "windows")]
        {
            run_command_with_output("whoami", &["/groups"])
                .map(|o| String::from_utf8_lossy(&o.stdout).contains("S-1-16-12288"))
                .unwrap_or(false)
        }
        #[cfg(target_os = "linux")]
        {
            run_command_with_output("id", &["-u"])
                .map(|o| String::from_utf8_lossy(&o.stdout).trim() == "0")
                .unwrap_or(false)
        }
        #[cfg(target_os = "macos")]
        {
            run_command_with_output("id", &["-u"])
                .map(|o| String::from_utf8_lossy(&o.stdout).trim() == "0")
                .unwrap_or(false)
        }
        #[cfg(not(any(target_os = "windows", target_os = "linux", target_os = "macos")))]
        {
            false
        }
    }
}

fn seconds_until(target_time: NaiveTime, now: NaiveTime) -> u64 {
    let target_seconds = target_time.num_seconds_from_midnight() as u64;
    let now_seconds = now.num_seconds_from_midnight() as u64;

    if target_seconds >= now_seconds {
        target_seconds - now_seconds
    } else {
        (24 * 3600) - (now_seconds - target_seconds)
    }
}

fn execute_action(action: &ActionType) -> Result<(), String> {
    match action {
        ActionType::Shutdown => {
            #[cfg(target_os = "windows")]
            { run_command("shutdown", &["/s", "/t", "0", "/c", "EnergyPy scheduled shutdown"]) }
            #[cfg(target_os = "linux")]
            { run_command("shutdown", &["-h", "+1"]) }
            #[cfg(target_os = "macos")]
            { run_command("shutdown", &["-h", "+1"]) }
        }
        ActionType::Restart => {
            #[cfg(target_os = "windows")]
            { run_command("shutdown", &["/r", "/t", "0", "/c", "EnergyPy scheduled restart"]) }
            #[cfg(target_os = "linux")]
            { run_command("shutdown", &["-r", "+1"]) }
            #[cfg(target_os = "macos")]
            { run_command("shutdown", &["-r", "+1"]) }
        }
        ActionType::Suspend => {
            #[cfg(target_os = "windows")]
            { run_command("rundll32.exe", &["powrprof.dll,SetSuspendState", "0", "1", "0"]) }
            #[cfg(target_os = "linux")]
            { run_command("systemctl", &["suspend"]) }
            #[cfg(target_os = "macos")]
            { run_command("pmset", &["sleepnow"]) }
        }
        ActionType::Hibernate => {
            #[cfg(target_os = "windows")]
            { run_command("shutdown", &["/h"]) }
            #[cfg(target_os = "linux")]
            { run_command("systemctl", &["hibernate"]) }
            #[cfg(target_os = "macos")]
            { run_command("pmset", &["sleepnow"]) }
        }
        ActionType::Lock => {
            #[cfg(target_os = "windows")]
            { run_command("rundll32.exe", &["user32.dll,LockWorkStation"]) }
            #[cfg(target_os = "linux")]
            { run_command("loginctl", &["lock-session"]) }
            #[cfg(target_os = "macos")]
            { run_command("pmset", &["displaysleepnow"]) }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveTime;

    #[test]
    fn seconds_until_same_time_is_zero() {
        let t = NaiveTime::from_hms_opt(12, 0, 0).unwrap();
        assert_eq!(seconds_until(t, t), 0);
    }

    #[test]
    fn seconds_until_future_time() {
        let now = NaiveTime::from_hms_opt(12, 0, 0).unwrap();
        let target = NaiveTime::from_hms_opt(12, 30, 0).unwrap();
        assert_eq!(seconds_until(target, now), 1800);
    }

    #[test]
    fn seconds_until_past_time_rolls_to_next_day() {
        let now = NaiveTime::from_hms_opt(12, 0, 0).unwrap();
        let target = NaiveTime::from_hms_opt(11, 0, 0).unwrap();
        assert_eq!(seconds_until(target, now), 23 * 3600);
    }

    #[test]
    fn action_type_serializes_lowercase() {
        assert_eq!(serde_json::to_string(&ActionType::Shutdown).unwrap(), "\"shutdown\"");
        assert_eq!(serde_json::to_string(&ActionType::Hibernate).unwrap(), "\"hibernate\"");
    }
}
