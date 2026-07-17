# Traspaso para nuevo chat de Codex

## Protocolo permanente de trabajo

Cada vez que Codex trabaje en este proyecto debe:

1. Leer este archivo de handoff al empezar o retomar una sesion.
2. Usarlo como fuente de continuidad del proyecto.
3. Actualizarlo al terminar cualquier bloque de trabajo relevante.
4. Dejar anotados:
   - que se ha hecho;
   - que queda pendiente;
   - comandos importantes ya ejecutados o pendientes;
   - decisiones tomadas;
   - bloqueos o limitaciones encontradas.

El objetivo es que el usuario no tenga que recordar manualmente el estado del proyecto entre sesiones.

## Contexto

El usuario quiere crear una app privada de registro/log/diario personal.

La app debe permitir guardar eventos relevantes del dia a dia, catalogarlos por fecha, tipo, ambito, personas, tags y otros campos, y hacer busquedas facilmente. La captura inicial sera mediante dictado o escritura en un chat de IA, que generara archivos compatibles para importar en la app.

## Carpeta final deseada

El usuario quiere que el repo viva en:

```text
D:\1. Proyectos\registro-personal-log
```

La sesion anterior no pudo escribir ahi porque Codex solo concedio permisos de lectura externos. Por eso el repo semilla se preparo temporalmente en la carpeta de Codex.

## Repo semilla ya creado

Ubicacion temporal:

```text
C:\Users\arkan\Documents\Codex\2026-07-17\llevo-mucho-tiempo-queriendo-crear-un\registro-personal-log
```

ZIP exportado:

```text
C:\Users\arkan\Documents\Codex\2026-07-17\llevo-mucho-tiempo-queriendo-crear-un\outputs\registro-personal-log.zip
```

## Archivos creados

```text
README.md
docs/JOURNAL_CHAT_SKILL.md
docs/PRODUCT_SPEC.md
docs/DATA_MODEL.md
docs/IMPORT_FORMAT.md
docs/HANDOFF_TO_NEW_CODEX_CHAT.md
examples/sample_import.jsonl
examples/sample_export.md
db/schema.sql
app/.gitkeep
importer/.gitkeep
.gitignore
```

## Decisiones tomadas

- La app debe funcionar inicialmente con un flujo de importacion desde chat.
- El formato principal de importacion sera JSONL.
- Cada entrada tendra `id` unico para importaciones idempotentes.
- Tambien tendra `content_hash` para detectar posibles duplicados por contenido.
- Se usara modo mixto:
  - entradas claras se generan directamente;
  - entradas ambiguas o sensibles pueden llevar notas o pedir confirmacion.
- `raw_input` no sera literal absoluto: sera una transcripcion fiel ligeramente limpiada.
- `body` sera la version redactada y legible de la entrada.
- Se anadio `cleanup_level`, por defecto `"light"`.
- La app importadora debe validar, recalcular hashes si hace falta y detectar conflictos.

## Arquitectura conceptual

```text
Chat con instrucciones .md
-> archivo JSONL compatible
-> importador validante
-> base de datos
-> busqueda/exportacion
```

## Decisiones tecnicas abiertas

Queda por decidir:

- confirmar SQLite como base inicial tras revisar sus limites;
- si usar Supabase/PostgreSQL, SQLite cifrado o self-hosted;
- autenticacion;
- cifrado;
- busqueda semantica;
- manejo de adjuntos.

Recomendacion previa:

- app web privada mobile-first;
- PostgreSQL como opcion robusta;
- Supabase para avanzar rapido, o self-hosted si prima privacidad/control;
- importador JSONL antes de meter IA dentro de la app.

## Siguiente paso recomendado

1. Abrir un nuevo chat de Codex usando como carpeta/proyecto:

```text
D:\1. Proyectos\registro-personal-log
```

2. Si la carpeta esta vacia, descomprimir o copiar alli el repo semilla.
3. Pedir al nuevo chat:

```text
Lee docs/HANDOFF_TO_NEW_CODEX_CHAT.md, docs/PRODUCT_SPEC.md, docs/DATA_MODEL.md, docs/IMPORT_FORMAT.md y docs/JOURNAL_CHAT_SKILL.md. Continuemos desde ahi.
```

4. Inicializar o revisar Git.
5. Hacer el primer commit cuando el usuario confirme.

## Estado actualizado 2026-07-17

El repo ya fue creado en GitHub:

```text
https://github.com/Hexabor/registro-personal-log
```

El commit inicial ya fue subido a `main`:

```text
5224439 Initial project seed
```

Despues se preparo GitHub Pages localmente con estos archivos:

```text
.github/workflows/pages.yml
site/index.html
site/styles.css
site/assets/flow.svg
```

Tambien se actualizo `README.md` para mencionar la carpeta `site/`.

Codex no pudo hacer `git add`, `commit` ni `push` porque la sesion no tenia permiso de escritura sobre `.git`. El usuario debe ejecutar en su terminal:

```powershell
cd "D:\1. Proyectos\registro-personal-log"

git add README.md .github/workflows/pages.yml site/index.html site/styles.css site/assets/flow.svg docs/HANDOFF_TO_NEW_CODEX_CHAT.md
git commit -m "Add GitHub Pages site"
git push
```

Luego activar GitHub Pages con workflow si no se activa solo:

```powershell
gh api -X POST repos/Hexabor/registro-personal-log/pages -f build_type=workflow
```

Si GitHub responde que Pages ya existe:

```powershell
gh api -X PUT repos/Hexabor/registro-personal-log/pages -f build_type=workflow
```

URL esperada:

```text
https://hexabor.github.io/registro-personal-log/
```

## Aclaraciones de producto 2026-07-17

- La captura se hara en ChatGPT, mediante dictado o conversacion natural y las instrucciones de `docs/JOURNAL_CHAT_SKILL.md`.
- La app no debe duplicar inicialmente una interfaz de captura ni integrar IA propia.
- El traspaso inicial sera: ChatGPT genera un archivo JSONL, el usuario lo abre o selecciona desde la app y la app valida, muestra una vista previa e importa.
- La app se usara principalmente desde un Pixel 10, por lo que la importacion, consulta, busqueda y revision deben disenarse mobile-first.
- El usuario lleva unos seis meses creando web apps, algunas complejas, y no ha trabajado antes con Python. No busca aprender a programar el stack en detalle: actua como product owner y delega la implementacion en Codex.
- El stack sigue abierto. La recomendacion mas reciente se recoge en `Revision de arquitectura por coste y mantenimiento` al final de este archivo.

Flujo corregido:

```text
ChatGPT + instrucciones de captura
-> archivo JSONL
-> apertura/seleccion desde la app en el Pixel
-> validacion y vista previa
-> importacion idempotente
-> busqueda, filtros y exportacion
```

## Stack aprobado y puntos pendientes

El usuario ha aprobado estas piezas:

1. React + TypeScript + Vite para una PWA mobile-first.
2. Hono como API TypeScript, portando y reorganizando la logica del importador existente.
3. Una unica fuente de datos central para que Pixel y ordenador consulten exactamente la misma informacion.

Continuan como propuestas pendientes de cerrar:

1. SQLite central como base de datos inicial.
2. Primer hito ejecutable en local, sin autenticacion.
3. Primer flujo de producto: seleccionar JSONL generado por ChatGPT, validar, previsualizar y confirmar la importacion.

Antes de materializar el stack, el usuario quiere revisar y comprender punto por punto al menos las tres primeras elecciones: que aporta cada tecnologia, como encaja en la arquitectura, que alternativas existen y que costes o limitaciones introduce.

## Perfil tecnico confirmado

El usuario ya ha construido una herramienta corporativa con este stack:

- frontend en HTML, CSS y JavaScript vanilla, organizado en modulos propios y sin build step;
- librerias puntuales como Papa Parse, pako.js y Google Identity Services;
- API REST escrita a mano en PHP contra MySQL;
- experiencia previa con IndexedDB mediante Dexie.js;
- Git y desarrollo asistido por Claude Code y Codex;
- sin experiencia previa con React, Vue, TypeScript, bundlers o frameworks de backend.

La familiaridad del usuario con el stack no debe condicionar la arquitectura: necesita comprender por que se elige cada pieza y sus costes, pero Codex implementara y mantendra el codigo. Por tanto, la recomendacion vuelve a priorizar coste total, fiabilidad, velocidad y mantenibilidad:

- React para una interfaz con varios estados coordinados: importacion, vista previa, conflictos, busqueda, filtros y detalle;
- TypeScript para reducir errores en el contrato de datos extenso;
- Vite para desarrollo, pruebas y compilacion de la PWA;
- PWA orientada al Pixel;
- API TypeScript para compartir lenguaje y contratos con el frontend;
- SQLite como almacenamiento inicial.

## Modelo de colaboracion

- El usuario actua como product owner y decide objetivos, prioridades y tradeoffs.
- Codex actua como equipo de desarrollo: propone arquitectura, implementa, prueba, documenta y mantiene.
- Las explicaciones deben centrarse en por que una alternativa ofrece mejor coste/resultado, no en ensenar al usuario a programarla.
- La complejidad de aprendizaje del usuario no es un criterio principal; si lo son la complejidad operativa, el riesgo, el coste de mantenimiento y la reversibilidad.

React, TypeScript, Vite y Hono ya estan confirmados. SQLite y las decisiones de despliegue, autenticacion y cifrado siguen pendientes de explicacion y confirmacion.

## Revision de arquitectura por coste y mantenimiento

Se han identificado tres preguntas antes de cerrar el stack:

1. Compartir el stack PHP/MySQL/vanilla de KPI Metrics o elegir el mejor stack para esta app.
2. Confirmar si SQLite cubre el acceso centralizado desde Pixel y otros dispositivos, y preparar el camino a PostgreSQL.
3. Justificar Python frente a un backend TypeScript de extremo a extremo.

Recomendacion actual pendiente de confirmacion:

- No reutilizar PHP solo por uniformidad con KPI Metrics. Ambos proyectos pueden compartir principios operativos, pero esta app puede usar un stack propio si reduce el coste total.
- Reducir la diversidad del nuevo proyecto usando TypeScript tanto en frontend como en backend. El importador Python actual es suficientemente pequeno para portarlo y no existe IA integrada ni procesamiento que requiera especialmente Python.
- Usar Hono como API TypeScript y compartir esquemas de validacion entre cliente y servidor.
- Mantener, si se confirma, SQLite inicialmente como base central en el servidor, no como una base distinta dentro de cada dispositivo. Pixel y escritorio accederan mediante la API.
- Evitar acceso a SQLite por red o desde varias instancias. El primer despliegue debe usar una sola instancia con almacenamiento persistente.
- Preparar migraciones, una capa de acceso a datos y un adaptador de busqueda para permitir SQLite -> PostgreSQL sin reescribir el dominio. JSONL seguira siendo la salida de recuperacion independiente de la base.
- La PWA sera inicialmente online-first; el modo offline con sincronizacion queda fuera del MVP.

Stack candidato resultante:

```text
React + TypeScript + Vite (PWA)
-> API TypeScript con Hono
-> SQLite central en primera fase
-> PostgreSQL si aparecen multiples instancias, concurrencia o necesidades operativas mayores
```

## Fase 0 completada 2026-07-18

Se ha creado el cimiento ejecutable de la aplicacion como monorepo pnpm:

```text
apps/web
  React 19 + TypeScript 7 + Vite 8

apps/api
  Hono 4 sobre Node.js

packages/contracts
  Zod 4 y tipos compartidos
```

Trabajo realizado:

- configuracion raiz de pnpm, TypeScript y Biome;
- lockfile reproducible y autorizacion limitada del script nativo de `esbuild`;
- endpoint `GET /api/health` en Hono;
- API limitada a `127.0.0.1` en desarrollo para evitar exposicion accidental a la red local;
- cliente React que valida la respuesta con el contrato compartido;
- proxy de Vite desde `/api` hacia Hono durante el desarrollo;
- pruebas de contrato, API y cliente;
- builds limpios de contratos, API y web;
- documentacion de arquitectura en `docs/ARCHITECTURE.md`;
- instrucciones de desarrollo en `README.md`.

Verificacion ejecutada:

```text
pnpm run verify
-> Biome: correcto
-> TypeScript: correcto
-> Vitest: 5 pruebas correctas
-> Build API: correcto
-> Build web: correcto
```

Tambien se comprobo el flujo en ejecucion:

```text
GET http://127.0.0.1:5173/ -> 200
GET http://127.0.0.1:5173/api/health -> status ok
```

La funcionalidad PWA avanzada se mantiene en su fase posterior; la fase 0 solo prepara la web mobile-first. SQLite continua pendiente de confirmacion y no se ha acoplado almacenamiento al cimiento.

Siguiente fase: portar a TypeScript el contrato completo de entrada y la logica del importador Python, preservando su comportamiento mediante pruebas de compatibilidad.
