import { serve } from "@hono/node-server";
import { app } from "./app.js";

const port = Number.parseInt(process.env.PORT ?? "8787", 10);
const hostname = process.env.API_HOST ?? "127.0.0.1";

serve({ fetch: app.fetch, hostname, port }, (info) => {
  console.log(`Registro personal API listening on http://${hostname}:${info.port}`);
});
