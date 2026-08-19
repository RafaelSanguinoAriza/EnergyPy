import { writable } from "svelte/store";

export interface CpuInfo {
  usage: number;
  cores: number[];
  frequency: number;
  name: string;
  temperature: number | null;
}

export interface MemoryInfo {
  total: number;
  used: number;
  available: number;
  percent: number;
  swap_total: number;
  swap_used: number;
}

export interface DiskInfo {
  name: string;
  mount_point: string;
  total: number;
  used: number;
  available: number;
  percent: number;
  file_system: string;
  is_removable: boolean;
  is_read_only: boolean;
}

export interface NetworkInfo {
  interface: string;
  received: number;
  transmitted: number;
}

export interface BatteryInfo {
  present: boolean;
  percent: number;
  charging: boolean;
  time_to_full: number | null;
  time_to_empty: number | null;
}

export interface ProcessInfo {
  pid: number;
  name: string;
  cpu: number;
  memory: number;
  memory_percent: number;
  exe: string;
  start_time: number;
  disk_read: number;
  disk_write: number;
}

export interface SystemStats {
  uptime_seconds: number;
  hostname: string;
  os: string;
  kernel: string;
  arch: string;
  cpu: CpuInfo;
  memory: MemoryInfo;
  disks: DiskInfo[];
  networks: NetworkInfo[];
  battery: BatteryInfo;
  top_processes: ProcessInfo[];
}

export const systemStats = writable<SystemStats | null>(null);
