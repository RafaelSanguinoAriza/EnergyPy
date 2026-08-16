<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import { formatPercent, formatFrequency } from "$lib/formatters";
  import { Cpu } from "@lucide/svelte";

  let { cpu }: {
    cpu: { usage: number; cores: number[]; frequency: number; name: string } | null;
  } = $props();
</script>

<Card class="p-4">
  <div class="flex items-center justify-between mb-3">
    <div class="flex items-center gap-2">
      <Cpu class="w-5 h-5 text-energy-500" />
      <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("cpu")}</h3>
    </div>
    {#if cpu}
      <span class="text-xs text-gray-400 dark:text-gray-500">{cpu.name}</span>
    {/if}
  </div>
  {#if cpu}
    <div class="space-y-3">
      <div>
        <div class="flex justify-between text-sm mb-1">
          <span class="text-gray-600 dark:text-gray-400">{$t("usage")}</span>
          <span class="font-mono font-bold text-lg">{formatPercent(cpu.usage)}</span>
        </div>
        <ProgressBar value={cpu.usage} color={cpu.usage > 80 ? "bg-red-500" : cpu.usage > 50 ? "bg-yellow-500" : "bg-energy-500"} />
      </div>
      <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>{cpu.cores.length} {$t("cores")}</span>
        <span>{formatFrequency(cpu.frequency)}</span>
      </div>
      {#if cpu.cores.length > 1}
        <div class="grid grid-cols-4 gap-1">
          {#each cpu.cores as core, i}
            <div class="text-center">
              <div class="text-[10px] text-gray-400">C{i}</div>
              <div class="h-1.5 bg-gray-200 dark:bg-slate-600 rounded-full overflow-hidden">
                <div class="h-full bg-energy-400 rounded-full transition-all" style="width: {core}%"></div>
              </div>
              <div class="text-[10px] font-mono">{core.toFixed(0)}%</div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {:else}
    <p class="text-sm text-gray-400">{$t("loading")}</p>
  {/if}
</Card>
