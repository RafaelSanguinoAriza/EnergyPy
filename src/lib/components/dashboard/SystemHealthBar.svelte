<script lang="ts">
  import { t } from "$lib/i18n";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import { Cpu, MemoryStick, HardDrive, Battery } from "@lucide/svelte";

  let { cpu, memory, disks, battery }: {
    cpu: { usage: number } | null;
    memory: { percent: number } | null;
    disks: Array<{ percent: number }>;
    battery: { present: boolean; percent: number } | null;
  } = $props();

  let cpuPercent = $derived(cpu?.usage ?? null);
  let memoryPercent = $derived(memory?.percent ?? null);
  let diskPercent = $derived(disks.length > 0 ? Math.max(...disks.map((d) => d.percent)) : null);
  let batteryPercent = $derived(battery?.present ? battery.percent : null);

  function barColor(percent: number | null): string {
    if (percent === null) return "bg-gray-400";
    if (percent > 80) return "bg-red-500";
    if (percent > 50) return "bg-yellow-500";
    return "bg-energy-500";
  }

  function metricColor(percent: number | null, base: string): string {
    if (percent === null) return "text-gray-400";
    if (percent > 80) return "text-red-500";
    if (percent > 50) return "text-yellow-500";
    return base;
  }
</script>

<div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Cpu class="w-4 h-4 text-energy-500" />
        <span class="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("cpu")}</span>
      </div>
      <span class="text-xl font-mono font-bold {metricColor(cpuPercent, 'text-energy-500')}">
        {cpuPercent !== null ? cpuPercent.toFixed(0) + "%" : "—"}
      </span>
    </div>
    <div class="mt-3">
      <ProgressBar value={cpuPercent ?? 0} size="sm" color={barColor(cpuPercent)} />
    </div>
  </div>

  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <MemoryStick class="w-4 h-4 text-purple-500" />
        <span class="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("memory")}</span>
      </div>
      <span class="text-xl font-mono font-bold {metricColor(memoryPercent, 'text-purple-500')}">
        {memoryPercent !== null ? memoryPercent.toFixed(0) + "%" : "—"}
      </span>
    </div>
    <div class="mt-3">
      <ProgressBar value={memoryPercent ?? 0} size="sm" color={barColor(memoryPercent)} />
    </div>
  </div>

  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <HardDrive class="w-4 h-4 text-blue-500" />
        <span class="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("disk")}</span>
      </div>
      <span class="text-xl font-mono font-bold {metricColor(diskPercent, 'text-blue-500')}">
        {diskPercent !== null ? diskPercent.toFixed(0) + "%" : "—"}
      </span>
    </div>
    <div class="mt-3">
      <ProgressBar value={diskPercent ?? 0} size="sm" color={barColor(diskPercent)} />
    </div>
  </div>

  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Battery class="w-4 h-4 text-yellow-500" />
        <span class="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("battery")}</span>
      </div>
      <span class="text-xl font-mono font-bold {metricColor(batteryPercent, 'text-yellow-500')}">
        {batteryPercent !== null ? batteryPercent.toFixed(0) + "%" : "—"}
      </span>
    </div>
    <div class="mt-3">
      <ProgressBar value={batteryPercent ?? 0} size="sm" color={barColor(batteryPercent)} />
    </div>
  </div>
</div>
