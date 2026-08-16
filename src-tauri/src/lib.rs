mod config;
mod power_manager;
mod system_monitor;

use std::fs;
use std::path::PathBuf;
use std::sync::Mutex;
use log::info;
use simplelog::{ConfigBuilder, LevelFilter, WriteLogger};
use tauri::{Emitter, Manager, State, menu::{MenuBuilder, MenuItemBuilder}};
use tauri::tray::TrayIconBuilder;
use chrono::NaiveTime;
use power_manager::{ActionType, PowerManager};
use system_monitor::SystemMonitor;

fn log_path() -> PathBuf {
    let base = if cfg!(target_os = "windows") {
        std::env::var("APPDATA")
            .or_else(|_| std::env::var("LOCALAPPDATA"))
            .unwrap_or_else(|_| ".".to_string())
    } else if cfg!(target_os = "linux") {
        std::env::var("XDG_CONFIG_HOME")
            .or_else(|_| std::env::var("HOME").map(|h| format!("{h}/.config")))
            .unwrap_or_else(|_| ".".to_string())
    } else {
        std::env::var("HOME").unwrap_or_else(|_| ".".to_string())
    };
    PathBuf::from(base).join("EnergyPy")
}

fn init_logger() {
    let dir = log_path();
    let _ = fs::create_dir_all(&dir);
    let path = dir.join("energypy.log");
    let config = ConfigBuilder::new()
        .set_time_format_rfc3339()
        .build();
    if let Ok(file) = fs::File::create(&path) {
        let _ = WriteLogger::init(LevelFilter::Info, config, file);
    }
}

struct AppState {
    monitor: Mutex<SystemMonitor>,
    power: PowerManager,
}

#[tauri::command]
fn get_system_stats(state: State<AppState>) -> system_monitor::SystemStats {
    state.monitor.lock().unwrap().get_stats()
}

fn parse_action_type(action_type: &str) -> Result<ActionType, String> {
    match action_type {
        "shutdown" => Ok(ActionType::Shutdown),
        "restart" => Ok(ActionType::Restart),
        "suspend" => Ok(ActionType::Suspend),
        "hibernate" => Ok(ActionType::Hibernate),
        "lock" => Ok(ActionType::Lock),
        _ => Err("Invalid action type".to_string()),
    }
}

#[tauri::command]
fn schedule_shutdown(state: State<AppState>, app: tauri::AppHandle, seconds: u64, action_type: String) -> Result<(), String> {
    let action = parse_action_type(&action_type)?;
    state.power.schedule(seconds, action, app);
    Ok(())
}

#[tauri::command]
fn schedule_at_time(state: State<AppState>, app: tauri::AppHandle, action_type: String, target_time: String) -> Result<u64, String> {
    let action = parse_action_type(&action_type)?;
    let time = NaiveTime::parse_from_str(&target_time, "%H:%M")
        .map_err(|e| format!("Invalid time: {}", e))?;
    state.power.schedule_at_time(action, time, app)
}

#[tauri::command]
fn cancel_shutdown(state: State<AppState>) -> bool {
    state.power.cancel()
}

#[tauri::command]
fn get_scheduled_action(state: State<AppState>) -> power_manager::ScheduledAction {
    state.power.get_scheduled()
}

#[tauri::command]
fn get_config() -> config::AppConfig {
    config::load_config()
}

#[tauri::command]
fn save_config(new_config: config::AppConfig) -> Result<(), String> {
    config::save_config(&new_config)
}

#[tauri::command]
fn exit_app(app: tauri::AppHandle) {
    app.exit(0);
}

#[tauri::command]
fn is_admin() -> bool {
    PowerManager::is_admin()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    init_logger();
    info!("EnergyPy started");

    let monitor = SystemMonitor::new();
    let power = PowerManager::new();

    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_autostart::init(
            tauri_plugin_autostart::MacosLauncher::LaunchAgent,
            Some(vec!["--autostart"]),
        ))
        .plugin(tauri_plugin_process::init())
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            let _ = app
                .get_webview_window("main")
                .map(|w| { let _ = w.show(); let _ = w.set_focus(); });
        }))
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .manage(AppState {
            monitor: Mutex::new(monitor),
            power,
        })
        .invoke_handler(tauri::generate_handler![
            get_system_stats,
            schedule_shutdown,
            schedule_at_time,
            cancel_shutdown,
            get_scheduled_action,
            get_config,
            save_config,
            exit_app,
            is_admin,
        ])
        .setup(|app| {
            let show_item = MenuItemBuilder::with_id("show", "Show EnergyPy").build(app)?;
            let quit_item = MenuItemBuilder::with_id("quit", "Quit").build(app)?;
            let menu = MenuBuilder::new(app)
                .item(&show_item)
                .separator()
                .item(&quit_item)
                .build()?;

            TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .menu(&menu)
                .tooltip("EnergyPy - Power Control")
                .on_menu_event(|app, event| {
                    match event.id().as_ref() {
                        "show" => {
                            if let Some(window) = app.get_webview_window("main") {
                                let _ = window.show();
                                let _ = window.set_focus();
                            }
                        }
                        "quit" => {
                            app.exit(0);
                        }
                        _ => {}
                    }
                })
                .on_tray_icon_event(|tray, event| {
                    if let tauri::tray::TrayIconEvent::Click { .. } = event {
                        if let Some(window) = tray.app_handle().get_webview_window("main") {
                            let _ = window.show();
                            let _ = window.set_focus();
                        }
                    }
                })
                .build(app)?;

            let app_for_close = app.handle().clone();
            if let Some(window) = app.get_webview_window("main") {
                let win = window.clone();
                window.on_window_event(move |event| {
                    if let tauri::WindowEvent::CloseRequested { api, .. } = event {
                        if config::load_config().minimize_to_tray {
                            api.prevent_close();
                            let _ = win.hide();
                        } else {
                            app_for_close.exit(0);
                        }
                    }
                });
            }

            let start_hidden = config::load_config().start_minimized
                || std::env::args().any(|a| a == "--autostart");
            if start_hidden {
                if let Some(window) = app.get_webview_window("main") {
                    let _ = window.hide();
                }
            }

            let app_handle = app.handle().clone();
            std::thread::spawn(move || {
                loop {
                    if let Some(state) = app_handle.try_state::<AppState>() {
                        let stats = state.monitor.lock().unwrap().get_stats();
                        let _ = app_handle.emit("system-stats", &stats);
                    }
                    std::thread::sleep(std::time::Duration::from_secs(2));
                }
            });

            let app_handle2 = app.handle().clone();
            std::thread::spawn(move || {
                loop {
                    if let Some(state) = app_handle2.try_state::<AppState>() {
                        let action = state.power.get_scheduled();
                        let _ = app_handle2.emit("countdown-tick", &action);
                    }
                    std::thread::sleep(std::time::Duration::from_secs(1));
                }
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
