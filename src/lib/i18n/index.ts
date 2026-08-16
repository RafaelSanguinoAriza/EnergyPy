import { writable, derived } from "svelte/store";
import en from "./en.json";
import es from "./es.json";

export type Language = "en" | "es";

const translations: Record<Language, Record<string, string>> = { en, es };

export const currentLang = writable<Language>("en");

export const t = derived(currentLang, ($lang) => {
  const dict = translations[$lang] || translations.en;
  return (key: string, params?: Record<string, string | number>): string => {
    let text = dict[key] || key;
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        text = text.replace(`{${k}}`, String(v));
      }
    }
    return text;
  };
});

export const availableLanguages = [
  { value: "en" as Language, label: "English" },
  { value: "es" as Language, label: "Español" },
];
