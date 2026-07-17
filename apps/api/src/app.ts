import { AppInfoSchema } from "@registro/contracts";
import { Hono } from "hono";

export const app = new Hono().get("/api/health", (context) => {
  const response = AppInfoSchema.parse({
    status: "ok",
    service: "registro-personal-log-api",
    version: "0.1.0",
  });

  return context.json(response);
});

export type AppType = typeof app;
