import { writable } from "svelte/store";

export interface ScheduledAction {
  action_type: string;
  total_seconds: number;
  remaining_seconds: number;
  active: boolean;
}

export const scheduledAction = writable<ScheduledAction>({
  action_type: "shutdown",
  total_seconds: 0,
  remaining_seconds: 0,
  active: false,
});
