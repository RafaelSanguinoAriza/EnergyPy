<script lang="ts">
  import { t } from "$lib/i18n";
  import ProgressBar from "../ui/ProgressBar.svelte";
  import Button from "../ui/Button.svelte";
  import { formatTimeRemaining } from "$lib/formatters";
  import { cancelShutdown } from "$lib/tauri";
  import { Clock, XCircle } from "@lucide/svelte";
  import type { ScheduledAction } from "$lib/stores/countdown";

  let { action }: {
    action: ScheduledAction;
  } = $props();

  let actionLabels = $derived<Record<string, string>>({
    shutdown: $t("shutdown"),
    restart: $t("restart"),
    suspend: $t("suspend"),
    hibernate: $t("hibernate"),
    lock: $t("lock"),
  });

  let progress = $derived(
    action.total_seconds > 0
      ? ((action.total_seconds - action.remaining_seconds) / action.total_seconds) * 100
      : 0
  );

  async function handleCancel() {
    try {
      await cancelShutdown();
    } catch (e) {
      console.error("Failed to cancel:", e);
    }
  }
</script>

<div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6 {action.active ? 'animate-glow' : ''}">
  <div class="flex items-center gap-2 mb-4">
    <Clock class="w-5 h-5 text-energy-500 {action.active ? 'animate-pulse-soft' : ''}" />
    <h3 class="font-semibold">{$t("countdown")}</h3>
  </div>

  {#if action.active}
    <div class="text-center mb-4">
      <div class="text-5xl font-mono font-bold text-energy-500 mb-2">
        {formatTimeRemaining(action.remaining_seconds)}
      </div>
      <div class="text-sm text-gray-500 dark:text-gray-400">
        {actionLabels[action.action_type] ?? action.action_type} {$t("in_progress")}
      </div>
    </div>

    <ProgressBar value={progress} size="lg" />
    <div class="text-xs text-gray-400 text-center mt-2">
      {formatTimeRemaining(action.remaining_seconds)} {$t("remaining_of")} {formatTimeRemaining(action.total_seconds)}
    </div>

    <div class="mt-4 flex justify-center">
      <Button variant="danger" onclick={handleCancel}>
        <XCircle class="w-4 h-4" />
        {$t("cancel")}
      </Button>
    </div>
  {:else}
    <div class="text-center py-8">
      <div class="text-5xl font-mono font-bold text-gray-300 dark:text-gray-600 mb-2">--:--:--</div>
      <p class="text-sm text-gray-400">{$t("no_action_scheduled")}</p>
    </div>
  {/if}
</div>
