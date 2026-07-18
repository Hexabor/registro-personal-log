# Registro personal log

App privada para capturar, importar, consultar y exportar registros personales estructurados.

El proyecto nace con una idea central: poder dictar entradas en un chat de IA, convertirlas en registros compatibles y guardarlas en una base de datos segura, versatil y exportable.

## Empezar en un ordenador nuevo

En un equipo donde el repositorio todavia no existe, lo unico que necesitas llevar
contigo es la URL de este repo: GitHub muestra este README en la web sin clonar nada,
y desde aqui obtienes todo lo demas. Con Git, Node.js 24 y pnpm 11 instalados:

```powershell
git clone https://github.com/Hexabor/registro-personal-log.git
cd registro-personal-log
pnpm install --frozen-lockfile
pnpm verify
```

Despues abre Claude Code o Codex en la carpeta y pideles arrancar:

```text
Lee AGENTS.md y sigue el inicio obligatorio.
```

A partir de ahi el protocolo completo vive en el repo: `AGENTS.md` (reglas),
`docs/HANDOFF_TO_NEW_CODEX_CHAT.md` (checkpoint) y, para la puesta a punto detallada
de un equipo, `docs/CLAUDE_CODE_WELCOME.md`.

## Objetivos

- Capturar eventos, ideas, conversaciones, decisiones, tareas, reflexiones y observaciones diarias.
- Importar registros desde archivos JSONL generados por chats de IA.
- Evitar duplicidades mediante `id` unico y `content_hash`.
- Buscar por fecha, texto, tipo, ambito, personas, lugares, proyectos, tags e importancia.
- Exportar a CSV, Markdown y JSON.
- Mantener independencia del proveedor de IA.

## Flujo inicial

```text
Chat de captura
-> archivo JSONL compatible
-> importador validante
-> base de datos
-> busqueda y exportacion
```

## Estructura

```text
AGENTS.md
CLAUDE.md
apps/
  web/
  api/
packages/
  contracts/
docs/
  ARCHITECTURE.md
  CLAUDE_CODE_WELCOME.md
  HANDOFF_TO_NEW_CODEX_CHAT.md
  JOURNAL_CHAT_SKILL.md
  PRODUCT_SPEC.md
  DATA_MODEL.md
  IMPORT_FORMAT.md
examples/
  sample_import.jsonl
  sample_export.md
importer/
site/
```

## Continuidad entre agentes y equipos

El repositorio contiene su propio protocolo para continuar el trabajo desde Codex,
Claude Code u otro ordenador:

- `AGENTS.md`: reglas comunes de desarrollo y colaboracion;
- `CLAUDE.md`: instrucciones que Claude Code debe leer al entrar;
- `docs/CLAUDE_CODE_WELCOME.md`: preparacion completa de un equipo nuevo;
- `docs/HANDOFF_TO_NEW_CODEX_CHAT.md`: checkpoint exacto y siguiente tarea.

Todo agente debe revisar sus reglas y el handoff al principio y al final de cada
sesion. La guia de bienvenida solo es obligatoria al estrenar Claude Code, preparar
otro equipo o cambiar de forma relevante el entorno de trabajo.

## Importador local

El primer componente funcional esta en `importer/`. Permite importar JSONL compatible, guardar en SQLite y exportar a Markdown, CSV, JSON o JSONL.

Ejemplo:

```powershell
python importer/journal_importer.py --db data/journal.sqlite3 import examples/sample_import.jsonl
python importer/journal_importer.py --db data/journal.sqlite3 export --format markdown --output exports/journal.md
```

## GitHub Pages

La carpeta `site/` contiene la pagina estatica publica del proyecto. El workflow `.github/workflows/pages.yml` la despliega en GitHub Pages cuando se sube a `main`.

## Estado

Fase 0 de la aplicacion en marcha. El repositorio contiene un monorepo TypeScript con:

- `apps/web`: interfaz React creada con Vite;
- `apps/api`: API HTTP con Hono;
- `packages/contracts`: contratos compartidos y validados con Zod;
- el importador Python original como referencia de compatibilidad durante la migracion.

La base de datos, el alojamiento, la autenticacion y el cifrado siguen siendo decisiones separadas.

## Desarrollo de la app

Requisitos:

- Node.js 24 o compatible;
- pnpm 11.

Instalar dependencias y ejecutar web, API y contratos en modo desarrollo:

```powershell
pnpm install
pnpm dev
```

La web se abre en `http://localhost:5173` y redirige las peticiones `/api` a Hono en `http://localhost:8787`.

En desarrollo, Hono escucha solo en `127.0.0.1` para no exponer la API a la red local. Un despliegue en contenedor debera establecer explicitamente `API_HOST=0.0.0.0`.

Comprobacion completa:

```powershell
pnpm verify
```
