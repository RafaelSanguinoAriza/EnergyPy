<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import { formatUptime } from "$lib/formatters";
  import { Monitor } from "@lucide/svelte";

  let { hostname = "", os = "", kernel = "", arch = "", uptimeSeconds = 0 }: {
    hostname?: string;
    os?: string;
    kernel?: string;
    arch?: string;
    uptimeSeconds?: number;
  } = $props();

  let rows = $derived([
    { label: $t("os"), value: os },
    { label: $t("kernel"), value: kernel },
    { label: $t("hostname"), value: hostname },
    { label: $t("arch"), value: arch },
    { label: $t("uptime"), value: formatUptime(uptimeSeconds) },
  ]);
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    <Monitor class="w-5 h-5 text-sky-500" />
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("system")}</h3>
  </div>
  <div class="space-y-2">
    {#each rows as row}
      <div class="flex items-center justify-between gap-3 text-sm">
        <span class="text-gray-500 dark:text-gray-400 shrink-0">{row.label}</span>
        <span class="font-mono truncate max-w-[60%] text-right">{row.value || "—"}</span>
      </div>
    {/each}
  </div>
</Card>
