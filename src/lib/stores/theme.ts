import { writable, derived } from "svelte/store";

export type Theme = "light" | "dark" | "system";

export const theme = writable<Theme>("system");

function createOsTheme() {
  const { subscribe, set } = writable<"light" | "dark">("light");
  if (typeof window !== "undefined") {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const update = () => set(mq.matches ? "dark" : "light");
    update();
    mq.addEventListener("change", update);
  }
  return { subscribe };
}

const osTheme = createOsTheme();

export const resolvedTheme = derived([theme, osTheme], ([$theme, $os]) => {
  if ($theme !== "system") return $theme;
  return $os;
});

export function applyTheme(resolved: "light" | "dark") {
  if (resolved === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}
