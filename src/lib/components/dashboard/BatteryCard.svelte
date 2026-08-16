<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import { formatDurationShort } from "$lib/formatters";
  import { Battery, BatteryFull, BatteryWarning, BatteryLow, BatteryCharging } from "@lucide/svelte";

  let { battery }: {
    battery: { present: boolean; percent: number; charging: boolean; time_to_full: number | null; time_to_empty: number | null } | null;
  } = $props();

  let batteryIcon = $derived.by(() => {
    if (!battery?.present) return Battery;
    if (battery.charging) return BatteryCharging;
    if (battery.percent > 80) return BatteryFull;
    if (battery.percent > 30) return Battery;
    return BatteryLow;
  });

  let batteryColor = $derived(
    battery?.present ? (battery.percent > 50 ? "bg-energy-500" : battery.percent > 20 ? "bg-yellow-500" : "bg-red-500") : "bg-gray-400"
  );
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    {#if battery?.present}
      {@const Icon = batteryIcon}
      <Icon class="w-5 h-5 text-yellow-500" />
    {:else}
      <Battery class="w-5 h-5 text-gray-400" />
    {/if}
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("battery")}</h3>
  </div>
  {#if battery?.present}
    <div class="text-center py-2">
      <div class="text-3xl font-mono font-bold" class:text-green-500={battery.percent > 50} class:text-yellow-500={battery.percent <= 50 && battery.percent > 20} class:text-red-500={battery.percent <= 20}>
        {battery.percent.toFixed(0)}%
      </div>
      <div class="text-xs text-gray-400 mt-1">
        {battery.charging ? $t("charging") : $t("discharging")}
      </div>
    </div>
    <ProgressBar value={battery.percent} color={batteryColor} size="sm" />
    {#if battery.charging && battery.time_to_full}
      <div class="text-xs text-gray-400 mt-1 text-center">
        {$t("time_to_full")} {formatDurationShort(battery.time_to_full)}
      </div>
    {:else if !battery.charging && battery.time_to_empty}
      <div class="text-xs text-gray-400 mt-1 text-center">
        {$t("time_remaining")} {formatDurationShort(battery.time_to_empty)}
      </div>
    {/if}
  {:else}
    <p class="text-sm text-gray-400 text-center py-4">{$t("no_battery")}</p>
  {/if}
</Card>
