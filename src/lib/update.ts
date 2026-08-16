import { check, type Update } from "@tauri-apps/plugin-updater";
import { relaunch } from "@tauri-apps/plugin-process";

export async function checkForUpdate(): Promise<Update | null> {
  try {
    return await check();
  } catch {
    return null;
  }
}

export async function downloadAndInstall(update: Update) {
  await update.downloadAndInstall((event) => {
    console.log("Update progress:", event);
  });

  await relaunch();
}
