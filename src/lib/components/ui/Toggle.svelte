<script lang="ts">
  let { checked = false, onChange, label = "" }: {
    checked?: boolean;
    onChange?: (v: boolean) => void;
    label?: string;
  } = $props();

  function handleChange() {
    onChange?.(!checked);
  }
</script>

<div class="inline-flex items-center gap-3">
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    aria-label={label || "Toggle"}
    onclick={handleChange}
    onkeydown={(e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); handleChange(); } }}
    class="relative w-11 h-6 rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-energy-500/50 hover:scale-105 active:scale-95 cursor-pointer {checked ? 'bg-energy-500' : 'bg-gray-300 dark:bg-slate-600'}"
  >
    <div
      class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-all duration-200 {checked ? 'translate-x-5 bg-white' : 'translate-x-0'}"
    ></div>
  </button>
  {#if label}
    <button
      type="button"
      class="text-sm text-gray-700 dark:text-gray-300 cursor-pointer hover:underline"
      onclick={handleChange}
    >{label}</button>
  {/if}
</div>
