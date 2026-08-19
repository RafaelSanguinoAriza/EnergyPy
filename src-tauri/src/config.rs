use log::{error, warn};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub theme: String,
    pub language: String,
    pub notifications_enabled: bool,
    pub minimize_to_tray: bool,
    pub start_minimized: bool,
    pub auto_update: bool,
    pub auto_start: bool,
    pub refresh_rate: u64,
    pub last_tab: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            theme: "system".to_string(),
            language: "en".to_string(),
            notifications_enabled: true,
            minimize_to_tray: true,
            start_minimized: false,
            auto_update: true,
            auto_start: false,
            refresh_rate: 2,
            last_tab: "dashboard".to_string(),
        }
    }
}

fn config_path() -> PathBuf {
    #[cfg(target_os = "windows")]
    {
        let base = std::env::var("APPDATA").unwrap_or_else(|_| {
            std::env::var("LOCALAPPDATA").unwrap_or_else(|_| ".".to_string())
        });
        PathBuf::from(base).join("EnergyPy")
    }
    #[cfg(target_os = "linux")]
    {
        let base = std::env::var("XDG_CONFIG_HOME")
            .or_else(|_| std::env::var("HOME").map(|h| format!("{}/.config", h)))
            .unwrap_or_else(|_| ".".to_string());
        PathBuf::from(base).join("energypy")
    }
    #[cfg(target_os = "macos")]
    {
        let base = std::env::var("HOME").unwrap_or_else(|_| ".".to_string());
        PathBuf::from(base).join("Library").join("Application Support").join("EnergyPy")
    }
}

pub fn load_config() -> AppConfig {
    let mut config = AppConfig::default();
    let path = config_path().join("config.json");
    if path.exists() {
        match fs::read_to_string(&path) {
            Ok(content) => match serde_json::from_str::<AppConfig>(&content) {
                Ok(full) => return full,
                Err(e) => {
                    error!("Failed to parse config fully ({e}), merging partial values");
                    if let Ok(value) = serde_json::from_str::<serde_json::Value>(&content) {
                        if let Some(obj) = value.as_object() {
                            config.theme = obj.get("theme").and_then(|v| v.as_str()).unwrap_or(&config.theme).to_string();
                            config.language = obj.get("language").and_then(|v| v.as_str()).unwrap_or(&config.language).to_string();
                            config.notifications_enabled = obj.get("notifications_enabled").and_then(|v| v.as_bool()).unwrap_or(config.notifications_enabled);
                            config.minimize_to_tray = obj.get("minimize_to_tray").and_then(|v| v.as_bool()).unwrap_or(config.minimize_to_tray);
                            config.start_minimized = obj.get("start_minimized").and_then(|v| v.as_bool()).unwrap_or(config.start_minimized);
                            config.auto_update = obj.get("auto_update").and_then(|v| v.as_bool()).unwrap_or(config.auto_update);
                            config.auto_start = obj.get("auto_start").and_then(|v| v.as_bool()).unwrap_or(config.auto_start);
                            config.refresh_rate = obj.get("refresh_rate").and_then(|v| v.as_u64()).unwrap_or(config.refresh_rate);
                            config.last_tab = obj.get("last_tab").and_then(|v| v.as_str()).unwrap_or(&config.last_tab).to_string();
                        }
                    }
                }
            },
            Err(e) => warn!("Failed to read config: {e}"),
        }
    }
    config
}

pub fn save_config(config: &AppConfig) -> Result<(), String> {
    let dir = config_path();
    fs::create_dir_all(&dir).map_err(|e| format!("Failed to create config dir: {e}"))?;
    let path = dir.join("config.json");
    let content = serde_json::to_string_pretty(config).map_err(|e| format!("Failed to serialize config: {e}"))?;
    fs::write(&path, content).map_err(|e| format!("Failed to write config: {e}"))?;
    Ok(())
}
