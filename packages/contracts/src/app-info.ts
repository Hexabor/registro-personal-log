import { z } from "zod";

export const AppInfoSchema = z.object({
  status: z.literal("ok"),
  service: z.literal("registro-personal-log-api"),
  version: z.string().min(1),
});

export type AppInfo = z.infer<typeof AppInfoSchema>;
