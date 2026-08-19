<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import Skeleton from "../ui/Skeleton.svelte";
  import AnimatedNumber from "../ui/AnimatedNumber.svelte";
  import { formatBytes } from "$lib/formatters";
  import { HardDrive, Usb, Lock } from "@lucide/svelte";

  let { disks = [] }: {
    disks: Array<{ name: string; mount_point: string; total: number; used: number; available: number; percent: number; file_system: string; is_removable: boolean; is_read_only: boolean }>;
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
          <div class="flex items-center gap-1.5 mb-1">
            <span class="text-xs font-medium">{disk.mount_point}</span>
            {#if disk.file_system}
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 font-medium">{disk.file_system}</span>
            {/if}
            {#if disk.is_removable}
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400 font-medium flex items-center gap-0.5">
                <Usb class="w-2.5 h-2.5" />
                USB
              </span>
            {/if}
            {#if disk.is_read_only}
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-orange-100 dark:bg-orange-900/40 text-orange-600 dark:text-orange-400 font-medium flex items-center gap-0.5">
                <Lock class="w-2.5 h-2.5" />
                RO
              </span>
            {/if}
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
    <div class="space-y-3">
      {#each Array(2) as _}
        <div class="space-y-1">
          <Skeleton class="h-3 w-1/2" />
          <Skeleton class="h-2 w-full" />
          <Skeleton class="h-2 w-3/4" />
        </div>
      {/each}
    </div>
  {/if}
</Card>
