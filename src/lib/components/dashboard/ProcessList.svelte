<script lang="ts">
  import { t } from "$lib/i18n";
  import { formatBytes } from "$lib/formatters";
  import { goto } from "$app/navigation";
  import Card from "../ui/Card.svelte";
  import { ChevronRight, Activity } from "@lucide/svelte";

  let { processes = [] }: {
    processes: Array<{ pid: number; name: string; cpu: number; memory: number; memory_percent: number }>;
  } = $props();

  let sorted = $derived([...processes].sort((a, b) => b.cpu - a.cpu).slice(0, 5));
</script>

<Card class="p-4">
  <div class="flex items-center justify-between mb-3">
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("top_processes")}</h3>
    <button
      onclick={() => goto("/processes")}
      class="flex items-center gap-1 text-xs font-medium text-energy-600 dark:text-energy-400 hover:text-energy-700 dark:hover:text-energy-300 transition-colors"
    >
      {$t("view_all")}
      <ChevronRight class="w-3.5 h-3.5" />
    </button>
  </div>
  {#if sorted.length > 0}
    <div class="space-y-1">
      {#each sorted as proc, i}
        <div class="flex items-center gap-3 text-xs py-1.5 px-2 rounded border-l-2 border-transparent hover:bg-gray-50 dark:hover:bg-slate-700 hover:border-l-energy-500 transition-all duration-150">
          <span class="w-4 text-gray-400">{i + 1}</span>
          <span class="flex-1 truncate font-medium">{proc.name}</span>
          <span class="w-16 text-right font-mono text-energy-500">{proc.cpu.toFixed(1)}%</span>
          <span class="w-20 text-right font-mono text-purple-500">{formatBytes(proc.memory)}</span>
        </div>
      {/each}
    </div>
  {:else}
    <div class="flex flex-col items-center justify-center py-6 text-center">
      <Activity class="w-8 h-8 text-gray-300 dark:text-gray-600 mb-2" />
      <p class="text-sm text-gray-400">{$t("loading")}</p>
    </div>
  {/if}
</Card>
