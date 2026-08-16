import { writable } from "svelte/store";

export interface AppConfig {
  theme: string;
  language: string;
  notifications_enabled: boolean;
  minimize_to_tray: boolean;
  start_minimized: boolean;
  auto_update: boolean;
  last_tab: string;
}

export const defaultConfig: AppConfig = {
  theme: "system",
  language: "en",
  notifications_enabled: true,
  minimize_to_tray: true,
  start_minimized: false,
  auto_update: true,
  last_tab: "dashboard",
};

export const appConfig = writable<AppConfig>(defaultConfig);
