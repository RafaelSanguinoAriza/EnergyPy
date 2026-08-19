<script lang="ts">
  let { value = 0, max = 100, color = "bg-energy-500", size = "md", showLabel = false, glow = false, className = "" }: {
    value?: number;
    max?: number;
    color?: string;
    size?: string;
    showLabel?: boolean;
    glow?: boolean;
    className?: string;
  } = $props();

  let percent = $derived(max > 0 ? Math.min((value / max) * 100, 100) : 0);
  let height = $derived(size === "sm" ? "h-1.5" : size === "lg" ? "h-4" : "h-2.5");
</script>

<div class="w-full {className}">
  {#if showLabel}
    <div class="flex justify-between mb-1 text-xs text-gray-500 dark:text-gray-400">
      <span>{percent.toFixed(1)}%</span>
    </div>
  {/if}
  <div class="w-full bg-gray-200 dark:bg-slate-600 rounded-full {height} overflow-hidden">
    <div
      class="{color} {height} rounded-full transition-all duration-500 ease-out {glow ? 'animate-progress-glow' : ''}"
      style="width: {percent}%"
    ></div>
  </div>
</div>
