<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import Skeleton from "../ui/Skeleton.svelte";
  import AnimatedNumber from "../ui/AnimatedNumber.svelte";
  import { formatPercent, formatDurationShort } from "$lib/formatters";
  import { Battery, BatteryCharging, BatteryFull, BatteryWarning } from "@lucide/svelte";

  let { battery }: {
    battery: { present: boolean; percent: number; charging: boolean; time_to_full: number | null; time_to_empty: number | null } | null;
  } = $props();

  let batteryPercent = $derived(battery?.present ? battery.percent : null);

  let batteryColor = $derived(
    batteryPercent !== null
      ? batteryPercent < 20 ? "text-red-500" : batteryPercent < 50 ? "text-yellow-500" : "text-green-500"
      : "text-gray-400"
  );

  let barColor = $derived(
    batteryPercent !== null
      ? batteryPercent < 20 ? "bg-red-500" : batteryPercent < 50 ? "bg-yellow-500" : "bg-green-500"
      : "bg-gray-400"
  );

  let statusText = $derived(() => {
    if (!battery || !battery.present) return $t("battery_not_present");
    if (battery.charging && battery.time_to_full != null && battery.time_to_full > 0) {
      return `${$t("charging")} — ${formatDurationShort(battery.time_to_full)}`;
    }
    if (battery.charging) return $t("charging");
    if (!battery.charging && battery.time_to_empty != null && battery.time_to_empty > 0) {
      return `${$t("discharging")} — ${formatDurationShort(battery.time_to_empty)}`;
    }
    if (!battery.charging) return $t("discharging");
    return $t("battery");
  });

  let BatteryIcon = $derived(
    !battery || !battery.present ? Battery :
    battery.charging ? BatteryCharging :
    batteryPercent !== null && batteryPercent > 80 ? BatteryFull :
    batteryPercent !== null && batteryPercent < 20 ? BatteryWarning :
    Battery
  );
</script>

<Card class="p-4">
  <div class="flex items-center justify-between mb-3">
    <div class="flex items-center gap-2">
      <BatteryIcon class="w-5 h-5 text-yellow-500" />
      <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("battery")}</h3>
    </div>
    {#if batteryPercent !== null}
      <span class="text-xs text-gray-400 dark:text-gray-500">{statusText()}</span>
    {/if}
  </div>
  {#if battery && !battery.present}
    <div class="flex flex-col items-center justify-center py-6 text-center">
      <Battery class="w-10 h-10 text-gray-300 dark:text-gray-600 mb-2" />
      <p class="text-sm text-gray-400 dark:text-gray-500">{$t("battery_not_present")}</p>
    </div>
  {:else if battery}
    <div class="space-y-3">
      <div>
        <div class="flex justify-between text-sm mb-1">
          <span class="text-gray-600 dark:text-gray-400">{$t("usage")}</span>
          <span class="font-mono font-bold text-lg {batteryColor}"><AnimatedNumber value={batteryPercent ?? 0} suffix="%" /></span>
        </div>
        <ProgressBar value={batteryPercent ?? 0} color={barColor} />
      </div>
      <div class="grid grid-cols-2 gap-2 text-xs">
        <div class="text-center p-2 bg-gray-50 dark:bg-slate-700 rounded-lg">
          <div class="text-gray-500">{$t("battery")}</div>
          <div class="font-mono font-semibold {batteryColor}"><AnimatedNumber value={batteryPercent ?? 0} suffix="%" /></div>
        </div>
        <div class="text-center p-2 bg-gray-50 dark:bg-slate-700 rounded-lg">
          <div class="text-gray-500">{$t("status")}</div>
          <div class="font-mono font-semibold">{statusText()}</div>
        </div>
      </div>
      {#if batteryPercent !== null}
        <div class="flex items-center gap-2 text-xs text-gray-400 pt-1">
          {#if battery.charging && battery.time_to_full != null && battery.time_to_full > 0}
            <span>{$t("time_to_full")} {formatDurationShort(battery.time_to_full)}</span>
          {:else if !battery.charging && battery.time_to_empty != null && battery.time_to_empty > 0}
            <span>{$t("time_remaining")} {formatDurationShort(battery.time_to_empty)}</span>
          {/if}
        </div>
      {/if}
    </div>
  {:else}
    <div class="space-y-3">
      <Skeleton class="h-5 w-full" />
      <div class="grid grid-cols-2 gap-2">
        {#each Array(2) as _}
          <Skeleton class="h-12 w-full" variant="rect" />
        {/each}
      </div>
      <Skeleton class="h-3 w-2/3" />
    </div>
  {/if}
</Card>
