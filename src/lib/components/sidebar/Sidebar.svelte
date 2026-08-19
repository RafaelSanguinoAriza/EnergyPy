<script lang="ts">
  import { page } from "$app/stores";
  import { t } from "$lib/i18n";
  import { systemStats } from "$lib/stores/system";
  import { LayoutDashboard, Zap, Settings, Activity } from "@lucide/svelte";

  let navItems = $derived([
    { href: "/dashboard", label: $t("dashboard"), icon: LayoutDashboard },
    { href: "/power", label: $t("power_control"), icon: Zap },
    { href: "/processes", label: $t("processes"), icon: Activity },
    { href: "/settings", label: $t("settings"), icon: Settings },
  ]);

  let cpuUsage = $derived($systemStats?.cpu?.usage ?? null);

  let statusColor = $derived(
    cpuUsage !== null
      ? cpuUsage > 90 ? "bg-red-500" : cpuUsage > 70 ? "bg-yellow-500" : "bg-green-500"
      : "bg-gray-400"
  );
</script>

<aside class="w-16 lg:w-56 bg-white dark:bg-slate-800 border-r border-gray-200 dark:border-slate-700 flex flex-col items-center lg:items-stretch py-4 gap-1 shrink-0">
  <div class="px-3 lg:px-4 mb-6 flex items-center justify-center lg:justify-start gap-2">
    <div class="relative">
      <div class="w-8 h-8 bg-gradient-to-br from-energy-500 to-energy-700 rounded-lg flex items-center justify-center shadow-lg shadow-energy-500/20 transition-shadow duration-300">
        <svg viewBox="0 0 24 24" class="w-5 h-5 text-white fill-current drop-shadow-sm">
          <path d="M13 2L4 14h7l-2 8 10-12h-7l2-8z"/>
        </svg>
      </div>
      <span class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border-2 border-white dark:border-slate-800 {statusColor} transition-colors duration-500"></span>
    </div>
    <span class="hidden lg:block font-bold text-lg">EnergyPy</span>
  </div>

  {#each navItems as item}
    {@const Icon = item.icon}
    {@const active = $page.url.pathname === item.href}
    <div class="relative mx-2 group">
      {#if active}
        <div class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-energy-500 rounded-full"></div>
      {/if}
      <a
        href={item.href}
        title={item.label}
        class="flex items-center justify-center lg:justify-start gap-3 px-3 lg:px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 {active ? 'bg-energy-50 dark:bg-energy-900/20 text-energy-700 dark:text-energy-300' : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-700 hover:scale-[1.02] active:scale-[0.98]'}"
      >
        <Icon class="w-5 h-5 shrink-0 {active ? 'scale-110' : ''} transition-transform duration-150" />
        <span class="hidden lg:block">{item.label}</span>
      </a>
    </div>
  {/each}
</aside>
