<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import Skeleton from "../ui/Skeleton.svelte";
  import AnimatedNumber from "../ui/AnimatedNumber.svelte";
  import { formatFrequency } from "$lib/formatters";
  import { Cpu, Thermometer } from "@lucide/svelte";

  let { cpu }: {
    cpu: { usage: number; cores: number[]; frequency: number; name: string; temperature: number | null } | null;
  } = $props();

  let tempColor = $derived(
    cpu?.temperature != null
      ? cpu.temperature > 85 ? "text-red-500" : cpu.temperature > 65 ? "text-yellow-500" : "text-green-500"
      : "text-gray-400"
  );
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
          <span class="font-mono font-bold text-lg"><AnimatedNumber value={cpu.usage} suffix="%" /></span>
        </div>
        <ProgressBar value={cpu.usage} color={cpu.usage > 80 ? "bg-red-500" : cpu.usage > 50 ? "bg-yellow-500" : "bg-energy-500"} />
      </div>
      <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>{cpu.cores.length} {$t("cores")}</span>
        <span>{formatFrequency(cpu.frequency)}</span>
        {#if cpu.temperature != null}
          <span class="flex items-center gap-1 {tempColor}">
            <Thermometer class="w-3 h-3" />
            <AnimatedNumber value={cpu.temperature} decimals={0} suffix="°C" />
          </span>
        {/if}
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
    <div class="space-y-3">
      <Skeleton class="h-5 w-full" />
      <Skeleton class="h-3 w-2/3" />
      <div class="grid grid-cols-4 gap-1">
        {#each Array(8) as _}
          <Skeleton class="h-8 w-full" />
        {/each}
      </div>
    </div>
  {/if}
</Card>
