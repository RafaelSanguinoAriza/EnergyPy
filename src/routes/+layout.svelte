<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { resolvedTheme, applyTheme, theme } from "$lib/stores/theme";
  import { systemStats } from "$lib/stores/system";
  import { scheduledAction } from "$lib/stores/countdown";
  import { defaultConfig, appConfig } from "$lib/stores/config";
  import type { AppConfig } from "$lib/stores/config";
  import { currentLang, t } from "$lib/i18n/index";
  import { get } from "svelte/store";
  import { listenSystemStats, listenCountdown, cancelShutdown, exitApp, getConfig, saveConfig, listenPowerActionResult } from "$lib/tauri";
  import { checkForUpdate, downloadAndInstall } from "$lib/update";
  import { confirm as dialogConfirm } from "@tauri-apps/plugin-dialog";
  import { isPermissionGranted, requestPermission, sendNotification } from "@tauri-apps/plugin-notification";
  import Sidebar from "$lib/components/sidebar/Sidebar.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";

  let { children }: { children?: import("svelte").Snippet } = $props();

  let configReady = $state(false);

  const VALID_TABS = ["/dashboard", "/power", "/processes", "/settings"];

  $effect(() => {
    applyTheme($resolvedTheme);
  });

  $effect(() => {
    const path = $page.url.pathname;
    if (configReady && VALID_TABS.includes(path) && $appConfig.last_tab !== path) {
      const next = { ...$appConfig, last_tab: path };
      appConfig.set(next);
      saveConfig(next as unknown as Record<string, unknown>).catch(() => {});
    }
  });

  function handleKeydown(e: KeyboardEvent) {
    if (!e.ctrlKey && !e.metaKey) return;
    const target = e.target as HTMLElement | null;
    if (target) {
      const tag = target.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || target.isContentEditable) {
        return;
      }
    }
    switch (e.key.toLowerCase()) {
      case "c":
        cancelShutdown();
        break;
      case "t":
        theme.update((t) => t === "light" ? "dark" : t === "dark" ? "system" : "light");
        break;
      case "q":
        exitApp();
        break;
    }
  }

  async function ensureNotificationPermission(): Promise<boolean> {
    let granted = await isPermissionGranted();
    if (!granted) {
      granted = (await requestPermission()) === "granted";
    }
    return granted;
  }

  onMount(() => {
    getConfig().then(async (raw) => {
      const saved = raw as Partial<AppConfig>;
      if (saved.theme) theme.set(saved.theme as "light" | "dark" | "system");
      if (saved.language) currentLang.set(saved.language as "en" | "es");
      appConfig.set({ ...defaultConfig, ...saved });

      const lastTab = (saved.last_tab as string) || "dashboard";
      if (VALID_TABS.includes(lastTab) && $page.url.pathname !== lastTab) {
        goto(lastTab);
      }
      configReady = true;

      const cfg = get(appConfig);
      if (cfg.auto_update) {
        const update = await checkForUpdate();
        if (update) {
          const translate = get(t);
          const ok = await dialogConfirm(
            translate("update_available", { version: update.version }),
            { title: translate("update_title"), kind: "info" }
          );
          if (ok) {
            try {
              await downloadAndInstall(update);
            } catch (e) {
              console.error("Update failed:", e);
            }
          }
        }
      }
    });

    const unlistenStats = listenSystemStats((stats) => {
      systemStats.set(stats);
    });

    const unlistenCountdown = listenCountdown((action) => {
      scheduledAction.set(action);
    });

    const unlistenResult = listenPowerActionResult(async (result) => {
      const cfg = get(appConfig);
      if (!cfg.notifications_enabled) return;
      if (await ensureNotificationPermission()) {
        sendNotification({ title: "EnergyPy", body: result.message });
      }
    });

    document.addEventListener("keydown", handleKeydown);

    return () => {
      unlistenStats.then((f) => f());
      unlistenCountdown.then((f) => f());
      unlistenResult.then((f) => f());
      document.removeEventListener("keydown", handleKeydown);
    };
  });
</script>

<div class="flex h-screen overflow-hidden">
  <Sidebar />
  <main class="flex-1 overflow-y-auto bg-gray-50 dark:bg-slate-900 p-4 lg:p-6">
    {#key $page.url.pathname}
      <div in:fly={{ x: 30, duration: 250, delay: 100 }} out:fly={{ x: -30, duration: 200 }}>
        {#if children}
          {@render children()}
        {/if}
      </div>
    {/key}
    </main>
  </div>
  <Toast />
