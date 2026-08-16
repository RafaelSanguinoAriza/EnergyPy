<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import { formatBytes, formatPercent } from "$lib/formatters";
  import { MemoryStick } from "@lucide/svelte";

  let { memory }: {
    memory: { total: number; used: number; available: number; percent: number; swap_total: number; swap_used: number } | null;
  } = $props();
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    <MemoryStick class="w-5 h-5 text-purple-500" />
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("memory")}</h3>
  </div>
  {#if memory}
    <div class="space-y-2">
      <div class="flex justify-between text-sm mb-1">
        <span class="text-gray-600 dark:text-gray-400">{$t("usage")}</span>
        <span class="font-mono font-bold text-lg">{formatPercent(memory.percent)}</span>
      </div>
      <ProgressBar value={memory.percent} color={memory.percent > 80 ? "bg-red-500" : memory.percent > 50 ? "bg-yellow-500" : "bg-purple-500"} />
      <div class="grid grid-cols-3 gap-2 text-xs mt-3">
        <div class="text-center p-2 bg-gray-50 dark:bg-slate-700 rounded-lg">
          <div class="text-gray-500">{$t("total")}</div>
          <div class="font-mono font-semibold">{formatBytes(memory.total)}</div>
        </div>
        <div class="text-center p-2 bg-gray-50 dark:bg-slate-700 rounded-lg">
          <div class="text-gray-500">{$t("used")}</div>
          <div class="font-mono font-semibold">{formatBytes(memory.used)}</div>
        </div>
        <div class="text-center p-2 bg-gray-50 dark:bg-slate-700 rounded-lg">
          <div class="text-gray-500">{$t("available")}</div>
          <div class="font-mono font-semibold">{formatBytes(memory.available)}</div>
        </div>
      </div>
      {#if memory.swap_total > 0}
        <div class="text-xs text-gray-400 pt-1">
          Swap: {formatBytes(memory.swap_used)} / {formatBytes(memory.swap_total)}
        </div>
      {/if}
    </div>
  {:else}
    <p class="text-sm text-gray-400">{$t("loading")}</p>
  {/if}
</Card>
