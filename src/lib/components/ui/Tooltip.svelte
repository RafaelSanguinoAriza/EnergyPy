<script lang="ts">
  let { text = "", position = "top", children }: {
    text?: string;
    position?: "top" | "bottom" | "left" | "right";
    children?: import("svelte").Snippet;
  } = $props();

  let posClasses = $derived({
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2",
  }[position]);
</script>

<div class="relative inline-flex group/tip">
  {#if children}
    {@render children()}
  {/if}
  {#if text}
    <div class="absolute {posClasses} z-50 pointer-events-none opacity-0 group-hover/tip:opacity-100 transition-opacity duration-150">
      <div class="px-2 py-1 text-xs font-medium text-white bg-gray-900 dark:bg-gray-700 rounded-md shadow-lg whitespace-nowrap">
        {text}
      </div>
    </div>
  {/if}
</div>
