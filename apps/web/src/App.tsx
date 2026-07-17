import { useEffect, useState } from "react";
import { getAppInfo } from "./lib/api.js";
import "./styles.css";

type ApiState = "checking" | "ready" | "unavailable";

export function App() {
  const [apiState, setApiState] = useState<ApiState>("checking");

  useEffect(() => {
    const controller = new AbortController();

    getAppInfo((input, init) => fetch(input, { ...init, signal: controller.signal }))
      .then(() => setApiState("ready"))
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }
        setApiState("unavailable");
      });

    return () => controller.abort();
  }, []);

  const status = {
    checking: "Comprobando la conexion…",
    ready: "Web y API conectadas",
    unavailable: "La API no esta disponible",
  }[apiState];

  return (
    <main className="app-shell">
      <section className="intro" aria-labelledby="app-title">
        <p className="eyebrow">Fase 0 · Cimientos</p>
        <h1 id="app-title">Registro personal</h1>
        <p className="lede">
          Tu archivo privado para revisar, guardar y encontrar los registros generados en ChatGPT.
        </p>
      </section>

      <section className="system-status" aria-live="polite">
        <span className={`status-dot status-dot--${apiState}`} aria-hidden="true" />
        <div>
          <strong>{status}</strong>
          <p>React · TypeScript · Hono · contrato compartido</p>
        </div>
      </section>
    </main>
  );
}
