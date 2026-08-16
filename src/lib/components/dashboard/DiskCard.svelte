<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import { formatBytes } from "$lib/formatters";
  import { HardDrive } from "@lucide/svelte";

  let { disks = [] }: {
    disks: Array<{ name: string; mount_point: string; total: number; used: number; available: number; percent: number }>;
  } = $props();
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    <HardDrive class="w-5 h-5 text-blue-500" />
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("disk")}</h3>
  </div>
  {#if disks.length > 0}
    <div class="space-y-3">
      {#each disks as disk}
        <div>
          <div class="flex justify-between text-xs mb-1">
            <span class="font-medium">{disk.mount_point}</span>
            <span class="text-gray-500">{disk.name}</span>
          </div>
          <ProgressBar value={disk.percent} color={disk.percent > 85 ? "bg-red-500" : disk.percent > 60 ? "bg-yellow-500" : "bg-blue-500"} size="sm" />
          <div class="flex justify-between text-[11px] text-gray-400 mt-0.5">
            <span>{formatBytes(disk.used)} / {formatBytes(disk.total)}</span>
            <span>{formatBytes(disk.available)} {$t("free")}</span>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <p class="text-sm text-gray-400">{$t("loading")}</p>
  {/if}
</Card>
