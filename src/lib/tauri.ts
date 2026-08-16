import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import type { SystemStats } from "./stores/system";
import type { ScheduledAction } from "./stores/countdown";

export async function getSystemStats(): Promise<SystemStats> {
  return invoke("get_system_stats");
}

export async function scheduleShutdown(seconds: number, actionType: string): Promise<void> {
  return invoke("schedule_shutdown", { seconds, actionType });
}

export async function scheduleAtTime(actionType: string, targetTime: string): Promise<number> {
  return invoke("schedule_at_time", { actionType, targetTime });
}

export async function cancelShutdown(): Promise<boolean> {
  return invoke("cancel_shutdown");
}

export async function getScheduledAction(): Promise<ScheduledAction> {
  return invoke("get_scheduled_action");
}

export async function getConfig(): Promise<Record<string, unknown>> {
  return invoke("get_config");
}

export async function saveConfig(config: Record<string, unknown>): Promise<void> {
  return invoke("save_config", { newConfig: config });
}

export async function exitApp(): Promise<void> {
  return invoke("exit_app");
}

export async function isAdmin(): Promise<boolean> {
  return invoke("is_admin");
}

export interface ActionResult {
  success: boolean;
  message: string;
  action_type: string;
}

export function listenPowerActionResult(callback: (result: ActionResult) => void) {
  return listen<ActionResult>("power-action-result", (event) => {
    callback(event.payload);
  });
}

export function listenSystemStats(callback: (stats: SystemStats) => void) {
  return listen<SystemStats>("system-stats", (event) => {
    callback(event.payload);
  });
}

export function listenCountdown(callback: (action: ScheduledAction) => void) {
  return listen<ScheduledAction>("countdown-tick", (event) => {
    callback(event.payload);
  });
}
