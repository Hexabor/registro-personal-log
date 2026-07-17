# Importador local

Importador JSONL inicial para validar registros compatibles con `docs/JOURNAL_CHAT_SKILL.md`, guardarlos en SQLite y exportarlos.

## Uso

Inicializar base de datos:

```powershell
python importer/journal_importer.py --db data/journal.sqlite3 init
```

Importar JSONL:

```powershell
python importer/journal_importer.py --db data/journal.sqlite3 import examples/sample_import.jsonl
```

Exportar:

```powershell
python importer/journal_importer.py --db data/journal.sqlite3 export --format markdown --output exports/journal.md
python importer/journal_importer.py --db data/journal.sqlite3 export --format csv --output exports/journal.csv
python importer/journal_importer.py --db data/journal.sqlite3 export --format json --output exports/journal.json
```

## Comportamiento

- Recalcula siempre `content_hash`.
- Ignora una entrada repetida si llega con el mismo `id` y el mismo contenido.
- Marca conflicto si llega el mismo `id` con contenido distinto.
- Inserta entradas con el mismo `content_hash` y distinto `id`, pero guarda una advertencia `possible_duplicate_of`.
