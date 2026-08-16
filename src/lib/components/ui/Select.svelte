<script lang="ts">
  let { value = $bindable(""), options = [] as { value: string; label: string }[], onChange, label = "" }: {
    value?: string;
    options: { value: string; label: string }[];
    onChange?: (v: string) => void;
    label?: string;
  } = $props();

  let selectId = $state(crypto.randomUUID());
</script>

<div class="flex flex-col gap-1">
  {#if label}
    <label for={selectId} class="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</label>
  {/if}
  <select
    id={selectId}
    bind:value
    onchange={(e) => onChange?.((e.target as HTMLSelectElement).value)}
    class="px-3 py-2 rounded-lg border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-energy-500/50 hover:border-energy-400 dark:hover:border-energy-600 transition-colors duration-150 cursor-pointer"
  >
    {#each options as opt}
      <option value={opt.value}>{opt.label}</option>
    {/each}
  </select>
</div>
