<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import { formatBytes } from "$lib/formatters";

  let { processes = [] }: {
    processes: Array<{ pid: number; name: string; cpu: number; memory: number; memory_percent: number }>;
  } = $props();

  let sorted = $derived([...processes].sort((a, b) => b.cpu - a.cpu).slice(0, 10));
</script>

<Card class="p-4">
  <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-3">{$t("top_processes")}</h3>
  {#if sorted.length > 0}
    <div class="space-y-1">
      {#each sorted as proc, i}
        <div class="flex items-center gap-3 text-xs py-1.5 px-2 rounded hover:bg-gray-50 dark:hover:bg-slate-700">
          <span class="w-4 text-gray-400">{i + 1}</span>
          <span class="flex-1 truncate font-medium">{proc.name}</span>
          <span class="w-16 text-right font-mono text-energy-500">{proc.cpu.toFixed(1)}%</span>
          <span class="w-20 text-right font-mono text-purple-500">{formatBytes(proc.memory)}</span>
        </div>
      {/each}
    </div>
  {:else}
    <p class="text-sm text-gray-400">{$t("loading")}</p>
  {/if}
</Card>
