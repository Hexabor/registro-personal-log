import { describe, expect, it } from "vitest";
import { AppInfoSchema } from "./app-info.js";

describe("AppInfoSchema", () => {
  it("accepts the API health response", () => {
    expect(
      AppInfoSchema.parse({
        status: "ok",
        service: "registro-personal-log-api",
        version: "0.1.0",
      }),
    ).toEqual({
      status: "ok",
      service: "registro-personal-log-api",
      version: "0.1.0",
    });
  });

  it("rejects an unexpected service", () => {
    expect(() =>
      AppInfoSchema.parse({ status: "ok", service: "another-api", version: "0.1.0" }),
    ).toThrow();
  });
});
