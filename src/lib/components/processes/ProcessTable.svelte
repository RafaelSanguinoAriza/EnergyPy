<script lang="ts">
  import { t } from "$lib/i18n";
  import { formatBytes } from "$lib/formatters";
  import { killProcess } from "$lib/tauri";
  import { confirm as dialogConfirm } from "@tauri-apps/plugin-dialog";
  import { get } from "svelte/store";
  import { fade } from "svelte/transition";
  import { Search, X, ArrowUpDown, ArrowUp, ArrowDown, Trash2, Activity } from "@lucide/svelte";

  let { processes = [] }: {
    processes: Array<{
      pid: number; name: string; cpu: number; memory: number; memory_percent: number;
      exe: string; start_time: number; disk_read: number; disk_write: number;
    }>;
  } = $props();

  let searchQuery = $state("");
  let sortKey = $state<"name" | "cpu" | "memory" | "memory_percent">("cpu");
  let sortDir = $state<"asc" | "desc">("desc");
  let killingPid = $state<number | null>(null);

  let filtered = $derived.by(() => {
    let list = [...processes];
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter((p) => p.name.toLowerCase().includes(q) || String(p.pid).includes(q));
    }
    list.sort((a, b) => {
      let av = a[sortKey];
      let bv = b[sortKey];
      if (typeof av === "string") av = av.toLowerCase();
      if (typeof bv === "string") bv = bv.toLowerCase();
      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
    return list;
  });

  function toggleSort(key: typeof sortKey) {
    if (sortKey === key) {
      sortDir = sortDir === "asc" ? "desc" : "asc";
    } else {
      sortKey = key;
      sortDir = key === "name" ? "asc" : "desc";
    }
  }

  function sortIcon(key: typeof sortKey) {
    if (sortKey !== key) return ArrowUpDown;
    return sortDir === "asc" ? ArrowUp : ArrowDown;
  }

  async function handleKill(proc: { pid: number; name: string }) {
    const translate = get(t);
    const ok = await dialogConfirm(
      translate("kill_process_confirm", { name: proc.name, pid: proc.pid }),
      { title: translate("kill_process"), kind: "warning" }
    );
    if (!ok) return;

    killingPid = proc.pid;
    try {
      await killProcess(proc.pid);
    } catch (e) {
      console.error("Kill failed:", e);
    } finally {
      killingPid = null;
    }
  }

  async function handleKillAll() {
    const translate = get(t);
    const ok = await dialogConfirm(
      translate("kill_process_confirm", { name: `${filtered.length} ${translate("processes").toLowerCase()}`, pid: 0 }),
      { title: translate("kill_all_filtered"), kind: "warning" }
    );
    if (!ok) return;

    for (const proc of filtered) {
      try {
        await killProcess(proc.pid);
      } catch {
        // continue with next
      }
    }
  }

  function memColor(percent: number): string {
    if (percent > 5) return "text-red-500";
    if (percent > 2) return "text-yellow-500";
    return "text-purple-500";
  }

  function formatStartTime(ts: number): string {
    if (!ts) return "—";
    const now = Date.now() / 1000;
    const elapsed = now - ts;
    if (elapsed < 60) return `${Math.floor(elapsed)}s`;
    if (elapsed < 3600) return `${Math.floor(elapsed / 60)}m`;
    if (elapsed < 86400) return `${Math.floor(elapsed / 3600)}h`;
    return `${Math.floor(elapsed / 86400)}d`;
  }
</script>

<div class="space-y-4">
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
    <div class="relative flex-1 w-full">
      <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
      <input
        type="text"
        bind:value={searchQuery}
        placeholder={$t("search_processes")}
        class="w-full pl-9 pr-8 py-2 text-sm rounded-lg border border-gray-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-energy-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-800"
      />
      {#if searchQuery}
        <button
          onclick={() => (searchQuery = "")}
          class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <X class="w-4 h-4" />
        </button>
      {/if}
    </div>
    {#if filtered.length > 0}
      <button
        onclick={handleKillAll}
        class="flex items-center gap-2 px-3 py-2 text-xs font-medium text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors shrink-0"
      >
        <Trash2 class="w-3.5 h-3.5" />
        {$t("kill_all_filtered")} ({filtered.length})
      </button>
    {/if}
  </div>

  {#if filtered.length > 0}
    <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
      <div class="max-h-[500px] overflow-y-auto custom-scrollbar">
        <table class="w-full text-sm">
          <thead class="sticky top-0 z-10 bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600">
            <tr>
              <th class="text-left px-4 py-3">
                <button onclick={() => toggleSort("name")} class="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
                  {$t("name")}
                  {#if sortKey === "name"}
                    {@const SortIcon = sortIcon("name")}
                    <SortIcon class="w-3 h-3" />
                  {/if}
                </button>
              </th>
              <th class="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">PID</th>
              <th class="text-right px-4 py-3">
                <button onclick={() => toggleSort("cpu")} class="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 ml-auto">
                  {$t("cpu_percent")}
                  {#if sortKey === "cpu"}
                    {@const SortIcon = sortIcon("cpu")}
                    <SortIcon class="w-3 h-3" />
                  {/if}
                </button>
              </th>
              <th class="text-right px-4 py-3">
                <button onclick={() => toggleSort("memory")} class="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 ml-auto">
                  {$t("memory")}
                  {#if sortKey === "memory"}
                    {@const SortIcon = sortIcon("memory")}
                    <SortIcon class="w-3 h-3" />
                  {/if}
                </button>
              </th>
              <th class="text-right px-4 py-3">
                <button onclick={() => toggleSort("memory_percent")} class="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 ml-auto">
                  {$t("memory_percent")}
                  {#if sortKey === "memory_percent"}
                    {@const SortIcon = sortIcon("memory_percent")}
                    <SortIcon class="w-3 h-3" />
                  {/if}
                </button>
              </th>
              <th class="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("path")}</th>
              <th class="text-right px-4 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("start_time")}</th>
              <th class="text-center px-4 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">{$t("kill_process")}</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as proc (proc.pid)}
              <tr
                transition:fade={{ duration: 120 }}
                class="border-b border-gray-100 dark:border-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700/50 hover:border-l-2 hover:border-l-energy-400 transition-all duration-150"
              >
                <td class="px-4 py-2.5 font-medium truncate max-w-[200px]">{proc.name}</td>
                <td class="px-4 py-2.5 font-mono text-xs text-gray-500 dark:text-gray-400">{proc.pid}</td>
                <td class="px-4 py-2.5 text-right font-mono">
                  <span class={proc.cpu > 50 ? "text-red-500" : proc.cpu > 20 ? "text-yellow-500" : "text-energy-500"}>
                    {proc.cpu.toFixed(1)}%
                  </span>
                </td>
                <td class="px-4 py-2.5 text-right font-mono text-xs text-gray-700 dark:text-gray-300">{formatBytes(proc.memory)}</td>
                <td class="px-4 py-2.5 text-right font-mono text-xs {memColor(proc.memory_percent)}">
                  {proc.memory_percent.toFixed(1)}%
                </td>
                <td class="px-4 py-2.5 font-mono text-xs text-gray-500 dark:text-gray-400 truncate max-w-[150px]" title={proc.exe}>
                  {proc.exe || "—"}
                </td>
                <td class="px-4 py-2.5 text-right font-mono text-xs text-gray-500 dark:text-gray-400">
                  {formatStartTime(proc.start_time)}
                </td>
                <td class="px-4 py-2.5 text-center">
                  <button
                    onclick={() => handleKill(proc)}
                    disabled={killingPid === proc.pid}
                    class="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-md hover:bg-red-100 dark:hover:bg-red-900/40 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {#if killingPid === proc.pid}
                      <span class="animate-spin w-3 h-3 border border-red-400 border-t-transparent rounded-full"></span>
                    {:else}
                      <Trash2 class="w-3 h-3" />
                    {/if}
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {:else}
    <div class="flex flex-col items-center justify-center py-12 text-center">
      <Activity class="w-10 h-10 text-gray-300 dark:text-gray-600 mb-3" />
      <p class="text-sm text-gray-400 dark:text-gray-500">{$t("no_processes")}</p>
    </div>
  {/if}
</div>

<style>
  :global(.custom-scrollbar::-webkit-scrollbar) {
    width: 6px;
  }
  :global(.custom-scrollbar::-webkit-scrollbar-track) {
    background: transparent;
  }
  :global(.custom-scrollbar::-webkit-scrollbar-thumb) {
    background: #94a3b8;
    border-radius: 3px;
  }
  :global(.custom-scrollbar::-webkit-scrollbar-thumb:hover) {
    background: #64748b;
  }
  :global(.dark .custom-scrollbar::-webkit-scrollbar-thumb) {
    background: #475569;
  }
  :global(.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover) {
    background: #64748b;
  }
</style>
