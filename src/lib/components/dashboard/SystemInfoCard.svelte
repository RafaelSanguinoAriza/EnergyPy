<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import Skeleton from "../ui/Skeleton.svelte";
  import Tooltip from "../ui/Tooltip.svelte";
  import { formatUptime } from "$lib/formatters";
  import { Clock, Monitor, Cpu, Tag, Layers } from "@lucide/svelte";

  let { uptimeSeconds = 0, hostname = "", os = "", kernel = "", arch = "" }: {
    uptimeSeconds?: number;
    hostname?: string;
    os?: string;
    kernel?: string;
    arch?: string;
  } = $props();

  let statItems = $derived([
    { icon: Monitor, label: $t("os"), value: os, color: "text-sky-500" },
    { icon: Layers, label: $t("arch"), value: arch, color: "text-violet-500" },
    { icon: Cpu, label: $t("kernel"), value: kernel, color: "text-emerald-500" },
    { icon: Tag, label: $t("hostname"), value: hostname, color: "text-amber-500" },
  ]);

  let hasData = $derived(os || hostname);
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    <Monitor class="w-5 h-5 text-sky-500" />
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("system")}</h3>
  </div>
  {#if hasData}
    <div class="text-center py-2 mb-3">
      <div class="flex items-center justify-center gap-2 mb-1">
        <Clock class="w-4 h-4 text-orange-500" />
        <span class="text-xs text-gray-400">{$t("uptime")}</span>
      </div>
      <div class="text-3xl font-mono font-bold text-orange-500">{formatUptime(uptimeSeconds)}</div>
    </div>
    <div class="grid grid-cols-2 gap-2">
      {#each statItems as item}
        <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-3 flex flex-col gap-1">
          <div class="flex items-center gap-1.5">
            <item.icon class="w-3 h-3 {item.color}" />
            <span class="text-[10px] text-gray-500 dark:text-gray-400 uppercase tracking-wide">{item.label}</span>
          </div>
          <Tooltip text={item.value} position="bottom">
            <span class="text-xs font-mono font-semibold break-all leading-snug">{item.value || "—"}</span>
          </Tooltip>
        </div>
      {/each}
    </div>
  {:else}
    <div class="space-y-3">
      <Skeleton class="h-10 w-3/4 mx-auto" />
      <div class="grid grid-cols-2 gap-2">
        {#each Array(4) as _}
          <Skeleton class="h-14 w-full" variant="rect" />
        {/each}
      </div>
    </div>
  {/if}
</Card>
