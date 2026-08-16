<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import { formatUptime } from "$lib/formatters";
  import { Clock } from "@lucide/svelte";

  let { uptimeSeconds = 0, hostname = "", os = "" }: {
    uptimeSeconds?: number;
    hostname?: string;
    os?: string;
  } = $props();
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    <Clock class="w-5 h-5 text-orange-500" />
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("uptime")}</h3>
  </div>
  <div class="text-center py-2">
    <div class="text-3xl font-mono font-bold text-orange-500">{formatUptime(uptimeSeconds)}</div>
    <div class="text-xs text-gray-400 mt-1">{$t("uptime")}</div>
  </div>
  {#if hostname}
    <div class="flex justify-between text-xs text-gray-400 mt-2 pt-2 border-t border-gray-100 dark:border-slate-700">
      <span>{hostname}</span>
      <span class="truncate max-w-[200px]">{os}</span>
    </div>
  {/if}
</Card>
