# Bienvenida a Claude Code

Esta guia permite abrir el proyecto en un equipo nuevo y continuar sin depender del
historial de otro chat.

Es un documento de incorporacion: debe leerse completo la primera vez que Claude
Code trabaje en el proyecto, al preparar un equipo nuevo o cuando cambien la
instalacion o el protocolo. En las sesiones normales bastara con revisar
`../AGENTS.md`, `../CLAUDE.md` y el checkpoint actual.

## Enlaces del proyecto

- Repositorio: <https://github.com/Hexabor/registro-personal-log>
- Sitio informativo de GitHub Pages: <https://hexabor.github.io/registro-personal-log/>
- Carpeta habitual en Windows: `D:\1. Proyectos\registro-personal-log`
- Aplicacion local durante el desarrollo: <http://localhost:5173>
- Salud de la API local: <http://127.0.0.1:8787/api/health>

El sitio de GitHub Pages es actualmente una presentacion estatica del proyecto; no
es la aplicacion privada ni contiene datos personales.

## Que es este producto

Es una aplicacion web privada y mobile-first para importar registros personales
generados mediante una conversacion con ChatGPT. ChatGPT entrega un archivo JSONL;
la app lo validara, mostrara una vista previa y, en fases posteriores, lo guardara
en una fuente central consultable desde el Pixel y el ordenador.

El usuario es el product owner. No necesita mantener el codigo ni aprender cada
herramienta: el agente debe implementar, probar y explicar las decisiones por su
coste, resultado y mantenimiento.

## Estado y siguiente tarea

No copies el estado en esta guia porque quedaria obsoleto. La unica fuente de verdad
es la seccion `CHECKPOINT ACTUAL` de `HANDOFF_TO_NEW_CODEX_CHAT.md`.

Orden de lectura recomendado:

1. `../AGENTS.md`
2. `../CLAUDE.md`
3. `HANDOFF_TO_NEW_CODEX_CHAT.md`
4. `PRODUCT_SPEC.md`
5. `ARCHITECTURE.md`
6. Los documentos que el checkpoint enlace para la siguiente tarea.

## Preparar un equipo nuevo

Requisitos:

- Git.
- Node.js 24 o compatible.
- pnpm 11.
- Claude Code con acceso de lectura y escritura al repositorio.

Primera instalacion:

```powershell
git clone https://github.com/Hexabor/registro-personal-log.git
cd registro-personal-log
pnpm install --frozen-lockfile
pnpm run verify
```

Si el repositorio ya existe en el equipo:

```powershell
git status -sb
git fetch origin
git pull --ff-only origin main
pnpm install --frozen-lockfile
pnpm run verify
```

No ejecutar `git pull` si existen cambios locales sin identificar. Primero hay que
revisarlos y decidir con el usuario a quien pertenecen.

## Arrancar la aplicacion

```powershell
pnpm dev
```

Abrir <http://localhost:5173>. Vite envia `/api` a Hono, que escucha en
`127.0.0.1:8787`. Esta configuracion local evita exponer Node a la red y no debe
cambiarse solo para acceder desde otro dispositivo. El acceso real desde Pixel se
resolvera mediante el despliegue de una fase posterior.

## Mapa del repositorio

```text
apps/web                 React, interfaz mobile-first
apps/api                 API Hono sobre Node.js
packages/contracts       Esquemas Zod y tipos compartidos
docs                     Producto, arquitectura, formato y continuidad
examples                 JSONL y exportaciones de ejemplo
importer                 Importador Python legado, solo como referencia
site                     Pagina informativa publica de GitHub Pages
.github/workflows        Automatizacion de GitHub Pages
```

## Flujo de colaboracion

### Al inicio de cada sesion

1. Leer y revisar `AGENTS.md`, `CLAUDE.md` y el checkpoint.
2. Comprobar Git y sincronizar mediante avance directo (`--ff-only`).
3. Confirmar que se entiende la siguiente tarea y no abrir fases posteriores.
4. Si habra varios agentes a la vez, crear una rama separada por tarea.

### Durante el trabajo

- Mantener cambios pequenos y comprobables.
- Añadir pruebas junto al comportamiento.
- No mezclar decisiones de producto no aprobadas.
- Actualizar documentos cuando cambie la realidad del proyecto.
- Usar tokens visuales semanticos y mantener la logica separada del aspecto para
  que futuras skins sean baratas de incorporar.

### Al final de cada sesion

1. Ejecutar `pnpm run verify`.
2. Revisar `git diff` y `git status`.
3. Volver a revisar las reglas y actualizar el checkpoint con el estado exacto y la
   proxima tarea, incluso si el trabajo quedo a medias.
4. Hacer un commit descriptivo y subirlo cuando corresponda.
5. Indicar al usuario commit, rama, pruebas y cualquier pendiente.

## Mensaje sugerido para iniciar Claude Code

```text
Lee CLAUDE.md, AGENTS.md y el CHECKPOINT ACTUAL de
docs/HANDOFF_TO_NEW_CODEX_CHAT.md. Comprueba el estado de Git y resume en pocas
lineas el punto exacto del proyecto y la siguiente tarea antes de modificar nada.
Respeta el protocolo de cierre y actualiza el handoff al terminar.
```

## Reglas de privacidad

- No subir diarios reales, archivos JSONL personales, bases de datos, tokens,
  secretos ni credenciales.
- Usar solamente datos ficticios en ejemplos y pruebas.
- No exponer la API de desarrollo a la red local.
- Detenerse y consultar al usuario antes de cualquier decision que cambie el modelo
  de privacidad, alojamiento, autenticacion, cifrado o copias de seguridad.
