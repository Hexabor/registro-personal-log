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

## Stack todavia no decidido

Hay que decidir:

- framework de app;
- base de datos final;
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
- El usuario lleva unos seis meses creando web apps, algunas complejas, y no ha trabajado antes con Python. Le interesa aprender Python, pero conviene mantener una parte web familiar mientras aprende el backend o mejora el importador.
- El stack sigue abierto. Una opcion coherente para explorar es frontend web/PWA con TypeScript y backend Python reutilizando el importador existente, sin convertir esta recomendacion en una decision cerrada antes de preparar un pequeno prototipo.

Flujo corregido:

```text
ChatGPT + instrucciones de captura
-> archivo JSONL
-> apertura/seleccion desde la app en el Pixel
-> validacion y vista previa
-> importacion idempotente
-> busqueda, filtros y exportacion
```
