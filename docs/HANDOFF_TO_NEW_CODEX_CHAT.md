# Traspaso para nuevo chat de Codex

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

