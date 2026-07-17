# Registro personal log

App privada para capturar, importar, consultar y exportar registros personales estructurados.

El proyecto nace con una idea central: poder dictar entradas en un chat de IA, convertirlas en registros compatibles y guardarlas en una base de datos segura, versatil y exportable.

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
docs/
  JOURNAL_CHAT_SKILL.md
  PRODUCT_SPEC.md
  DATA_MODEL.md
  IMPORT_FORMAT.md
examples/
  sample_import.jsonl
  sample_export.md
db/
  schema.sql
app/
importer/
```

## Importador local

El primer componente funcional esta en `importer/`. Permite importar JSONL compatible, guardar en SQLite y exportar a Markdown, CSV, JSON o JSONL.

Ejemplo:

```powershell
python importer/journal_importer.py --db data/journal.sqlite3 import examples/sample_import.jsonl
python importer/journal_importer.py --db data/journal.sqlite3 export --format markdown --output exports/journal.md
```

## Estado

Fase inicial con contrato de datos definido y primer importador local funcional. Antes de construir la app completa, queda decidir stack de aplicacion, alojamiento, autenticacion y cifrado.
