<script lang="ts">
  import { toasts } from "$lib/stores/toast";
  import { fade, fly } from "svelte/transition";
  import { CheckCircle, XCircle, AlertTriangle, Info, X } from "@lucide/svelte";

  const iconMap = {
    success: CheckCircle,
    error: XCircle,
    warning: AlertTriangle,
    info: Info,
  };

  const colorMap = {
    success: "bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800 text-green-700 dark:text-green-300",
    error: "bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800 text-red-700 dark:text-red-300",
    warning: "bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-800 text-yellow-700 dark:text-yellow-300",
    info: "bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-300",
  };

  const iconColorMap = {
    success: "text-green-500",
    error: "text-red-500",
    warning: "text-yellow-500",
    info: "text-blue-500",
  };
</script>

<div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
  {#each $toasts as toast (toast.id)}
    {@const Icon = iconMap[toast.type]}
    <div
      in:fly={{ x: 40, duration: 250 }}
      out:fade={{ duration: 200 }}
      class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border shadow-lg min-w-[280px] max-w-[400px] {colorMap[toast.type]}"
    >
      <Icon class="w-5 h-5 shrink-0 {iconColorMap[toast.type]}" />
      <span class="text-sm font-medium flex-1">{toast.message}</span>
      <button
        onclick={() => toasts.remove(toast.id)}
        class="shrink-0 opacity-60 hover:opacity-100 transition-opacity"
      >
        <X class="w-4 h-4" />
      </button>
    </div>
  {/each}
</div>
