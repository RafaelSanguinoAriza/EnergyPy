<script lang="ts">
  import ActionSelector from "./ActionSelector.svelte";
  import Button from "../ui/Button.svelte";
  import { scheduleShutdown, scheduleAtTime } from "$lib/tauri";
  import { Calendar, Clock, AlertTriangle } from "@lucide/svelte";
  import { confirm as dialogConfirm } from "@tauri-apps/plugin-dialog";
  import { t } from "$lib/i18n";
  import { formatDurationShort } from "$lib/formatters";

  let { onScheduled }: {
    onScheduled?: () => void;
  } = $props();

  let actionType = $state("shutdown");
  let tab = $state<"time" | "hour">("time");
  let timeValue = $state(30);
  let timeUnit = $state(60);
  let targetHour = $state("12:00");
  let error = $state("");

  let totalSeconds = $derived(timeValue * timeUnit);

  let actionLabels = $derived<Record<string, string>>({
    shutdown: $t("shutdown"),
    restart: $t("restart"),
    suspend: $t("suspend"),
    hibernate: $t("hibernate"),
    lock: $t("lock"),
  });

  async function handleSchedule() {
    error = "";
    const label = actionLabels[actionType] ?? actionType;
    const confirmed = await dialogConfirm(
      $t("confirm_action", { action: label.toLowerCase() }),
      { title: $t("confirm_title"), kind: "warning" }
    );
    if (!confirmed) return;

    try {
      if (tab === "time") {
        await scheduleShutdown(totalSeconds, actionType);
      } else {
        await scheduleAtTime(actionType, targetHour);
      }
      onScheduled?.();
    } catch (e) {
      error = String(e);
    }
  }
</script>

<div class="space-y-6">
  <ActionSelector bind:value={actionType} />

  <div class="flex gap-2 mb-4">
    <button
      onclick={() => tab = "time"}
      class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors {tab === 'time' ? 'bg-energy-600 text-white' : 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-400'} cursor-pointer"
    >
      <Clock class="w-4 h-4" />
      {$t("schedule_by_time")}
    </button>
    <button
      onclick={() => tab = "hour"}
      class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors {tab === 'hour' ? 'bg-energy-600 text-white' : 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-400'} cursor-pointer"
    >
      <Calendar class="w-4 h-4" />
      {$t("schedule_at_hour")}
    </button>
  </div>

  {#if tab === "time"}
    <div class="flex items-center gap-2">
      <input
        type="number"
        bind:value={timeValue}
        min="1"
        max="86400"
        class="w-24 px-3 py-2 rounded-lg border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-center font-mono text-lg"
      />
      <select
        bind:value={timeUnit}
        class="px-3 py-2 rounded-lg border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-sm"
      >
        <option value={1}>{$t("seconds")}</option>
        <option value={60}>{$t("minutes")}</option>
        <option value={3600}>{$t("hours")}</option>
      </select>
    </div>
  {:else}
    <div>
      <input
        type="time"
        bind:value={targetHour}
        class="px-3 py-2 rounded-lg border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 font-mono text-lg"
      />
    </div>
  {/if}

  {#if error}
    <div class="flex items-center gap-2 text-red-500 text-sm">
      <AlertTriangle class="w-4 h-4" />
      {error}
    </div>
  {/if}

  <Button onclick={handleSchedule} class="w-full" size="lg">
    <Calendar class="w-4 h-4" />
    {tab === "time"
      ? `${$t("schedule")} ${actionLabels[actionType] ?? actionType} ${$t("in")} ${formatDurationShort(totalSeconds)}`
      : `${$t("schedule")} ${actionLabels[actionType] ?? actionType} ${$t("at")} ${targetHour}`}
  </Button>
</div>
