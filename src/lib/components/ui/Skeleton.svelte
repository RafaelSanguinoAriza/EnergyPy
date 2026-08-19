<script lang="ts">
  let { class: className = "", variant = "line" }: {
    class?: string;
    variant?: "line" | "circle" | "rect";
  } = $props();
</script>

{#if variant === "circle"}
  <div class="skeleton rounded-full {className}"></div>
{:else if variant === "rect"}
  <div class="skeleton rounded-xl {className}"></div>
{:else}
  <div class="skeleton rounded-lg {className}"></div>
{/if}

<style>
  .skeleton {
    background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
  }
  :global(.dark) .skeleton {
    background: linear-gradient(90deg, #334155 25%, #475569 50%, #334155 75%);
    background-size: 200% 100%;
  }
  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
</style>
