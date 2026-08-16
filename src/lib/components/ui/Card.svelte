<script lang="ts">
  let { class: className = "", children }: { class?: string; children?: import("svelte").Snippet } = $props();
</script>

<div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 {className}">
  {#if children}
    {@render children()}
  {/if}
</div>
