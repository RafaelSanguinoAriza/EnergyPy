<script lang="ts">
  import { t } from "$lib/i18n";
  import Card from "../ui/Card.svelte";
  import Skeleton from "../ui/Skeleton.svelte";
  import { formatBitsPerSecond } from "$lib/formatters";
  import { Network } from "@lucide/svelte";

  let { networks = [] }: {
    networks: Array<{ interface: string; received: number; transmitted: number }>;
  } = $props();
</script>

<Card class="p-4">
  <div class="flex items-center gap-2 mb-3">
    <Network class="w-5 h-5 text-cyan-500" />
    <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("network")}</h3>
  </div>
  {#if networks.length > 0}
    <div class="space-y-2">
      {#each networks as net}
        <div class="flex items-center justify-between p-2 bg-gray-50 dark:bg-slate-700 rounded-lg">
          <span class="text-xs font-medium">{net.interface}</span>
          <div class="flex gap-3 text-xs">
            <span class="text-green-500">↓ {formatBitsPerSecond(net.received)}</span>
            <span class="text-blue-500">↑ {formatBitsPerSecond(net.transmitted)}</span>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="space-y-2">
      {#each Array(3) as _}
        <Skeleton class="h-10 w-full" variant="rect" />
      {/each}
    </div>
  {/if}
</Card>
