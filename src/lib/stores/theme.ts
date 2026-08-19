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

let prevResolved: "light" | "dark" | null = null;

export function applyTheme(resolved: "light" | "dark") {
  if (prevResolved !== null && prevResolved !== resolved) {
    document.body.classList.add("theme-transitioning");
    setTimeout(() => {
      document.body.classList.remove("theme-transitioning");
    }, 250);
  }
  prevResolved = resolved;

  if (resolved === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}
