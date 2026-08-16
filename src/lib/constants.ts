export const ROUTES = {
  DASHBOARD: "/dashboard",
  POWER: "/power",
  SETTINGS: "/settings",
} as const;

export const TIME_UNITS = [
  { value: 1, label: "seconds" },
  { value: 60, label: "minutes" },
  { value: 3600, label: "hours" },
] as const;

export const ACTION_TYPES = [
  { value: "shutdown", label: "Shutdown", icon: "Power" },
  { value: "restart", label: "Restart", icon: "RotateCw" },
  { value: "suspend", label: "Suspend", icon: "Moon" },
  { value: "hibernate", label: "Hibernate", icon: "Sleep" },
  { value: "lock", label: "Lock", icon: "Lock" },
] as const;
