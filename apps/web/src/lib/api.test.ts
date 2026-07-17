import { describe, expect, it, vi } from "vitest";
import { getAppInfo } from "./api.js";

describe("getAppInfo", () => {
  it("validates the shared health contract", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          status: "ok",
          service: "registro-personal-log-api",
          version: "0.1.0",
        }),
        { status: 200, headers: { "content-type": "application/json" } },
      ),
    );

    await expect(getAppInfo(fetcher)).resolves.toEqual({
      status: "ok",
      service: "registro-personal-log-api",
      version: "0.1.0",
    });
  });

  it("rejects an unavailable API", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(null, { status: 503 }));

    await expect(getAppInfo(fetcher)).rejects.toThrow("estado 503");
  });
});
