<script lang="ts">
  import { t } from "$lib/i18n";
  import { scheduledAction } from "$lib/stores/countdown";
  import { goto } from "$app/navigation";
  import ScheduleForm from "$lib/components/power/ScheduleForm.svelte";
  import CountdownTimer from "$lib/components/power/CountdownTimer.svelte";
  import { Zap } from "@lucide/svelte";

  function handleScheduled() {}
</script>

<div class="max-w-2xl mx-auto space-y-6">
  <div class="flex items-center gap-3">
    <div class="w-10 h-10 bg-gradient-to-br from-energy-400 to-energy-600 rounded-xl flex items-center justify-center shadow-lg shadow-energy-500/20">
      <Zap class="w-5 h-5 text-white" />
    </div>
    <div>
      <h1 class="text-2xl font-bold">{$t("power_control")}</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400">{$t("power_subtitle")}</p>
    </div>
  </div>

  <CountdownTimer action={$scheduledAction} />

  {#if !$scheduledAction.active}
    <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6">
      <h2 class="text-lg font-semibold mb-4">{$t("new_schedule")}</h2>
      <ScheduleForm onScheduled={handleScheduled} />
    </div>
  {/if}
</div>
