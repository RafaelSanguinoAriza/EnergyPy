<script lang="ts">
  import { t } from "$lib/i18n";
  import { appConfig, defaultConfig } from "$lib/stores/config";
  import { currentLang, availableLanguages } from "$lib/i18n/index";
  import { theme } from "$lib/stores/theme";
  import { saveConfig } from "$lib/tauri";
  import Toggle from "$lib/components/ui/Toggle.svelte";
  import Select from "$lib/components/ui/Select.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import ThemeToggle from "$lib/components/theme/ThemeToggle.svelte";
  import { Settings } from "@lucide/svelte";

  let saving = $state(false);

  async function handleSave() {
    saving = true;
    try {
      await saveConfig($appConfig as unknown as Record<string, unknown>);
    } catch (e) {
      console.error("Failed to save config:", e);
    }
    saving = false;
  }

  function handleReset() {
    appConfig.set(defaultConfig);
    currentLang.set("en");
    theme.set("system");
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
  </div>

  <div class="flex gap-3 justify-end">
    <Button variant="ghost" onclick={handleReset}>{$t("reset_to_defaults")}</Button>
    <Button onclick={handleSave} disabled={saving}>
      {saving ? $t("saving") : $t("save_settings")}
    </Button>
  </div>
</div>
