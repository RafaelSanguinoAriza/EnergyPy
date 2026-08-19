<script lang="ts">
  import { t } from "$lib/i18n";
  import { appConfig, defaultConfig } from "$lib/stores/config";
  import { currentLang, availableLanguages } from "$lib/i18n/index";
  import { theme } from "$lib/stores/theme";
  import { saveConfig, enableAutostart, disableAutostart, getConfig } from "$lib/tauri";
  import { toasts } from "$lib/stores/toast";
  import Toggle from "$lib/components/ui/Toggle.svelte";
  import Select from "$lib/components/ui/Select.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import ThemeToggle from "$lib/components/theme/ThemeToggle.svelte";
  import { Settings, Info, ExternalLink, Code2 } from "@lucide/svelte";
  import { open } from "@tauri-apps/plugin-shell";
  import { onMount } from "svelte";

  let saving = $state(false);
  let savedConfig = $state<Record<string, unknown> | null>(null);

  const refreshRateOptions = [
    { value: "1", label: "1s" },
    { value: "2", label: "2s" },
    { value: "3", label: "3s" },
    { value: "5", label: "5s" },
    { value: "10", label: "10s" },
  ];

  const EDITABLE_KEYS = ["theme", "language", "notifications_enabled", "minimize_to_tray", "start_minimized", "auto_update", "auto_start", "refresh_rate"] as const;

  let hasUnsavedChanges = $derived(() => {
    if (!savedConfig) return false;
    const raw = $appConfig as unknown as Record<string, unknown>;
    const current = EDITABLE_KEYS.reduce((obj, k) => ({ ...obj, [k]: raw[k] }), {} as Record<string, unknown>);
    const saved = EDITABLE_KEYS.reduce((obj, k) => ({ ...obj, [k]: savedConfig![k] }), {} as Record<string, unknown>);
    return JSON.stringify(current) !== JSON.stringify(saved);
  });

  onMount(() => {
    getConfig().then((raw) => {
      savedConfig = raw as Record<string, unknown>;
    });
  });

  async function handleSave() {
    saving = true;
    try {
      await saveConfig($appConfig as unknown as Record<string, unknown>);
      const raw = $appConfig as unknown as Record<string, unknown>;
      savedConfig = EDITABLE_KEYS.reduce((obj, k) => ({ ...obj, [k]: raw[k] }), {} as Record<string, unknown>);
      toasts.success($t("save_settings"));
    } catch (e) {
      console.error("Failed to save config:", e);
      toasts.error(String(e));
      saving = false;
      return;
    }

    try {
      if ($appConfig.auto_start) {
        await enableAutostart();
      } else {
        await disableAutostart();
      }
    } catch (e) {
      console.warn("Autostart toggle failed (non-critical):", e);
    }

    saving = false;
  }

  function handleReset() {
    appConfig.set(defaultConfig);
    currentLang.set("en");
    theme.set("system");
    toasts.info($t("reset_to_defaults"));
  }

  function updateConfig(key: string, value: unknown) {
    appConfig.update((c) => ({ ...c, [key]: value }));
  }
</script>

<div class="max-w-2xl mx-auto space-y-6">
  <div class="flex items-center gap-3">
    <div class="w-10 h-10 bg-gradient-to-br from-energy-400 to-energy-600 rounded-xl flex items-center justify-center shadow-lg shadow-energy-500/20">
      <Settings class="w-5 h-5 text-white" />
    </div>
    <div>
      <h1 class="text-2xl font-bold">{$t("settings")}</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400">{$t("settings_subtitle")}</p>
    </div>
  </div>

  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6 space-y-6">
    <div>
      <h2 class="text-sm font-semibold uppercase tracking-wide text-gray-500 mb-4">{$t("general")}</h2>
      <div class="space-y-4">
        <Select
          label={$t("language")}
          options={availableLanguages}
          bind:value={$currentLang}
          onChange={(v) => { currentLang.set(v as "en" | "es"); updateConfig("language", v); }}
        />
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-700 dark:text-gray-300">{$t("notifications")}</span>
          <Toggle
            checked={$appConfig.notifications_enabled}
            onChange={(v) => updateConfig("notifications_enabled", v)}
          />
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-700 dark:text-gray-300">{$t("minimize_to_tray")}</span>
          <Toggle
            checked={$appConfig.minimize_to_tray}
            onChange={(v) => updateConfig("minimize_to_tray", v)}
          />
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-700 dark:text-gray-300">{$t("start_minimized")}</span>
          <Toggle
            checked={$appConfig.start_minimized}
            onChange={(v) => updateConfig("start_minimized", v)}
          />
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-700 dark:text-gray-300">{$t("auto_update")}</span>
          <Toggle
            checked={$appConfig.auto_update}
            onChange={(v) => updateConfig("auto_update", v)}
          />
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-700 dark:text-gray-300">{$t("auto_start")}</span>
          <Toggle
            checked={$appConfig.auto_start}
            onChange={(v) => updateConfig("auto_start", v)}
          />
        </div>
        <Select
          label={$t("refresh_rate")}
          options={refreshRateOptions}
          value={String($appConfig.refresh_rate)}
          onChange={(v) => updateConfig("refresh_rate", Number(v))}
        />
      </div>
    </div>

    <div class="border-t border-gray-200 dark:border-slate-700 pt-6">
      <h2 class="text-sm font-semibold uppercase tracking-wide text-gray-500 mb-4">{$t("appearance")}</h2>
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-700 dark:text-gray-300">{$t("theme")}</span>
        <ThemeToggle bind:value={$theme} onChange={(v) => { theme.set(v as "light" | "dark" | "system"); updateConfig("theme", v); }} />
      </div>
    </div>

    <div class="border-t border-gray-200 dark:border-slate-700 pt-6">
      <h2 class="text-sm font-semibold uppercase tracking-wide text-gray-500 mb-4">{$t("keyboard_shortcuts")}</h2>
      <div class="space-y-2">
        {#each [
          { keys: "Ctrl + C", desc: $t("cancel_scheduled") },
          { keys: "Ctrl + T", desc: $t("toggle_theme") },
          { keys: "Ctrl + Q", desc: $t("quit_app") },
        ] as shortcut}
          <div class="flex items-center justify-between py-1.5 px-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
            <span class="text-sm text-gray-600 dark:text-gray-400">{shortcut.desc}</span>
            <kbd class="px-2 py-0.5 text-xs font-mono bg-gray-200 dark:bg-slate-600 rounded">{shortcut.keys}</kbd>
          </div>
        {/each}
      </div>
    </div>

    <div class="border-t border-gray-200 dark:border-slate-700 pt-6">
      <div class="flex items-center gap-2 mb-4">
        <Info class="w-4 h-4 text-gray-500" />
        <h2 class="text-sm font-semibold uppercase tracking-wide text-gray-500">{$t("about")}</h2>
      </div>
      <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-5 space-y-4">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-gradient-to-br from-energy-400 to-energy-600 rounded-xl flex items-center justify-center shadow-lg shadow-energy-500/20">
            <span class="text-white font-bold text-lg">EP</span>
          </div>
          <div>
            <h3 class="font-bold text-lg text-gray-800 dark:text-gray-100">EnergyPy</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">{$t("version")} 2.0.1 · MIT</p>
          </div>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{$t("about_description")}</p>
        <div class="flex flex-col gap-2 pt-1">
          <div class="flex items-center gap-2 text-sm">
            <span class="text-gray-500 dark:text-gray-400 font-medium">{$t("version")}:</span>
            <span class="text-gray-700 dark:text-gray-200">2.0.1</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="text-gray-500 dark:text-gray-400 font-medium">{$t("license")}:</span>
            <span class="text-gray-700 dark:text-gray-200">MIT</span>
          </div>
          <button
            onclick={() => open("https://github.com/RafaelSanguinoAriza")}
            class="flex items-center gap-2 text-sm text-energy-600 dark:text-energy-400 hover:text-energy-700 dark:hover:text-energy-300 transition-colors w-fit"
          >
            <Code2 class="w-4 h-4" />
            <span>Rafael David Sanguino Ariza</span>
            <ExternalLink class="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="flex gap-3 justify-end items-center">
    {#if hasUnsavedChanges()}
      <span class="text-xs text-amber-500 dark:text-amber-400 font-medium animate-unsaved-pulse">Unsaved changes</span>
    {/if}
    <Button variant="ghost" onclick={handleReset}>{$t("reset_to_defaults")}</Button>
    <Button onclick={handleSave} disabled={saving}>
      {saving ? $t("saving") : $t("save_settings")}
    </Button>
  </div>
</div>
