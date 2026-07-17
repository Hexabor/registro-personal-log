import { type AppInfo, AppInfoSchema } from "@registro/contracts";

export async function getAppInfo(fetcher: typeof fetch = fetch): Promise<AppInfo> {
  const response = await fetcher("/api/health");

  if (!response.ok) {
    throw new Error(`La API respondio con el estado ${response.status}`);
  }

  return AppInfoSchema.parse(await response.json());
}
