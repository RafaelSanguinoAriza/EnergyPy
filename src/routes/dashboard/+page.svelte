<script lang="ts">
  import { t } from "$lib/i18n";
  import { systemStats } from "$lib/stores/system";
  import CpuCard from "$lib/components/dashboard/CpuCard.svelte";
  import MemoryCard from "$lib/components/dashboard/MemoryCard.svelte";
  import DiskCard from "$lib/components/dashboard/DiskCard.svelte";
  import NetworkCard from "$lib/components/dashboard/NetworkCard.svelte";
  import BatteryCard from "$lib/components/dashboard/BatteryCard.svelte";
  import ProcessList from "$lib/components/dashboard/ProcessList.svelte";
  import SystemInfoCard from "$lib/components/dashboard/SystemInfoCard.svelte";
  import { LayoutDashboard } from "@lucide/svelte";

  const stagger = [0, 60, 120, 180, 240, 300, 360];
</script>

<div class="space-y-4">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 bg-gradient-to-br from-energy-400 to-energy-600 rounded-xl flex items-center justify-center shadow-lg shadow-energy-500/20 shrink-0">
        <LayoutDashboard class="w-5 h-5 text-white" />
      </div>
      <div>
        <h1 class="text-2xl font-bold">{$t("dashboard")}</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">{$t("dashboard_subtitle")}</p>
      </div>
    </div>
    <div class="flex items-center gap-2 text-sm text-gray-400">
      <span class="relative flex h-2.5 w-2.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-energy-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-energy-500"></span>
      </span>
      <span>{$t("live")}</span>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="lg:col-span-3 animate-fade-in-up" style="animation-delay: {stagger[0]}ms">
      <CpuCard cpu={$systemStats?.cpu ?? null} />
    </div>
    <div class="lg:col-span-1 animate-fade-in-up" style="animation-delay: {stagger[1]}ms">
      <SystemInfoCard
        uptimeSeconds={$systemStats?.uptime_seconds ?? 0}
        hostname={$systemStats?.hostname ?? ""}
        os={$systemStats?.os ?? ""}
        kernel={$systemStats?.kernel ?? ""}
        arch={$systemStats?.arch ?? ""}
      />
    </div>

    <div class="lg:col-span-2 animate-fade-in-up" style="animation-delay: {stagger[2]}ms">
      <MemoryCard memory={$systemStats?.memory ?? null} />
    </div>
    <div class="lg:col-span-2 animate-fade-in-up" style="animation-delay: {stagger[3]}ms">
      <NetworkCard networks={$systemStats?.networks ?? []} />
    </div>

    <div class="lg:col-span-2 animate-fade-in-up" style="animation-delay: {stagger[4]}ms">
      <DiskCard disks={$systemStats?.disks ?? []} />
    </div>
    <div class="lg:col-span-2 animate-fade-in-up" style="animation-delay: {stagger[5]}ms">
      <BatteryCard battery={$systemStats?.battery ?? null} />
    </div>

    <div class="md:col-span-2 lg:col-span-4 animate-fade-in-up" style="animation-delay: {stagger[6]}ms">
      <ProcessList processes={$systemStats?.top_processes ?? []} />
    </div>
  </div>
</div>
