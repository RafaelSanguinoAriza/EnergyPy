import { writable } from "svelte/store";

export interface AppConfig {
  theme: string;
  language: string;
  notifications_enabled: boolean;
  minimize_to_tray: boolean;
  start_minimized: boolean;
  auto_update: boolean;
  auto_start: boolean;
  refresh_rate: number;
  last_tab: string;
}

export const defaultConfig: AppConfig = {
  theme: "system",
  language: "en",
  notifications_enabled: true,
  minimize_to_tray: true,
  start_minimized: false,
  auto_update: true,
  auto_start: false,
  refresh_rate: 2,
  last_tab: "dashboard",
};

export const appConfig = writable<AppConfig>(defaultConfig);
