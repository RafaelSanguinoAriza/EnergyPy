<script lang="ts">
  import { t } from "$lib/i18n";
  import { systemStats } from "$lib/stores/system";
  import CpuCard from "$lib/components/dashboard/CpuCard.svelte";
  import MemoryCard from "$lib/components/dashboard/MemoryCard.svelte";
  import DiskCard from "$lib/components/dashboard/DiskCard.svelte";
  import NetworkCard from "$lib/components/dashboard/NetworkCard.svelte";
  import UptimeCard from "$lib/components/dashboard/UptimeCard.svelte";
  import BatteryCard from "$lib/components/dashboard/BatteryCard.svelte";
  import ProcessList from "$lib/components/dashboard/ProcessList.svelte";
  import SystemHealthBar from "$lib/components/dashboard/SystemHealthBar.svelte";
  import SystemInfoCard from "$lib/components/dashboard/SystemInfoCard.svelte";
  import { LayoutDashboard } from "@lucide/svelte";
</script>

<div class="space-y-6">
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

  <SystemHealthBar
    cpu={$systemStats?.cpu ?? null}
    memory={$systemStats?.memory ?? null}
    disks={$systemStats?.disks ?? []}
    battery={$systemStats?.battery ?? null}
  />

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="lg:col-span-2">
      <CpuCard cpu={$systemStats?.cpu ?? null} />
    </div>
    <div class="lg:col-span-2">
      <MemoryCard memory={$systemStats?.memory ?? null} />
    </div>
    <div class="lg:col-span-2">
      <DiskCard disks={$systemStats?.disks ?? []} />
    </div>
    <div>
      <NetworkCard networks={$systemStats?.networks ?? []} />
    </div>
    <div>
      <BatteryCard battery={$systemStats?.battery ?? null} />
    </div>
    <div class="lg:col-span-2">
      <UptimeCard uptimeSeconds={$systemStats?.uptime_seconds ?? 0} hostname={$systemStats?.hostname ?? ""} os={$systemStats?.os ?? ""} />
    </div>
    <div class="lg:col-span-2">
      <SystemInfoCard
        hostname={$systemStats?.hostname ?? ""}
        os={$systemStats?.os ?? ""}
        kernel={$systemStats?.kernel ?? ""}
        arch={$systemStats?.arch ?? ""}
        uptimeSeconds={$systemStats?.uptime_seconds ?? 0}
      />
    </div>
    <div class="md:col-span-2 lg:col-span-4">
      <ProcessList processes={$systemStats?.top_processes ?? []} />
    </div>
  </div>
</div>
