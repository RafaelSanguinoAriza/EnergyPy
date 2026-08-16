<script lang="ts">
  import { t } from "$lib/i18n";
  import { resolvedTheme, applyTheme } from "$lib/stores/theme";
  import { Sun, Moon, Monitor } from "@lucide/svelte";
  import type { Component } from "svelte";

  let { value = $bindable("system"), onChange }: {
    value?: string;
    onChange?: (v: string) => void;
  } = $props();

  let themes = $derived([
    { value: "light", label: $t("light"), icon: Sun as Component },
    { value: "dark", label: $t("dark"), icon: Moon as Component },
    { value: "system", label: $t("system"), icon: Monitor as Component },
  ]);

  function select(v: string) {
    value = v;
    onChange?.(v);
  }
</script>

<div class="flex gap-1 bg-gray-100 dark:bg-slate-700 rounded-lg p-1">
  {#each themes as theme}
    {@const Icon = theme.icon}
    <button
      onclick={() => select(theme.value)}
      class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all {value === theme.value ? 'bg-white dark:bg-slate-600 shadow-sm text-gray-900 dark:text-gray-100' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'} cursor-pointer"
    >
      <Icon class="w-3.5 h-3.5" />
      <span class="hidden sm:inline">{theme.label}</span>
    </button>
  {/each}
</div>
