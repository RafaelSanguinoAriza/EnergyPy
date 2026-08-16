<script lang="ts">
  import { t } from "$lib/i18n";
  import { Power, RotateCw, Moon, Lock } from "@lucide/svelte";
  import type { Component } from "svelte";

  let { value = $bindable("shutdown"), onChange }: {
    value?: string;
    onChange?: (v: string) => void;
  } = $props();

  let actions = $derived([
    { value: "shutdown", label: $t("shutdown"), icon: Power as Component },
    { value: "restart", label: $t("restart"), icon: RotateCw as Component },
    { value: "suspend", label: $t("suspend"), icon: Moon as Component },
    { value: "hibernate", label: $t("hibernate"), icon: Moon as Component },
    { value: "lock", label: $t("lock"), icon: Lock as Component },
  ]);

  function select(v: string) {
    value = v;
    onChange?.(v);
  }
</script>

<div class="grid grid-cols-5 gap-2">
  {#each actions as action}
    {@const Icon = action.icon}
    <button
      onclick={() => select(action.value)}
      class="flex flex-col items-center gap-1.5 p-3 rounded-xl border-2 transition-all {value === action.value ? 'border-energy-500 bg-energy-50 dark:bg-energy-900/20' : 'border-gray-200 dark:border-slate-600 hover:border-gray-300 dark:hover:border-slate-500'} cursor-pointer"
    >
      <Icon class="w-5 h-5 {value === action.value ? 'text-energy-600' : 'text-gray-500 dark:text-gray-400'}" />
      <span class="text-xs font-medium {value === action.value ? 'text-energy-700 dark:text-energy-300' : 'text-gray-600 dark:text-gray-400'}">{action.label}</span>
    </button>
  {/each}
</div>
