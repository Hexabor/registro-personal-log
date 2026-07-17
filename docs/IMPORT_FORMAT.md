# Formato de importacion

## Formato principal

El formato de importacion principal es JSONL: un objeto JSON por linea.

Motivos:

- permite volcados incrementales;
- es facil de generar por chats de IA;
- se puede procesar linea a linea;
- evita rehacer archivos enormes;
- funciona bien para importaciones repetidas.

## Nombre recomendado

```text
journal_import_YYYYMMDD_HHMM.jsonl
```

Ejemplo:

```text
journal_import_20260717_1842.jsonl
```

## Reglas de importacion

1. Leer cada linea como JSON independiente.
2. Validar campos obligatorios.
3. Recalcular `content_hash` si viene como `sha256:pending`.
4. Comprobar si `id` ya existe.
5. Insertar solo entradas nuevas.
6. Registrar conflictos y posibles duplicados.

## Regla de hash

Calcular SHA-256 sobre esta concatenacion normalizada:

```text
event_date|title|body|type|people|tags
```

La normalizacion deberia:

- recortar espacios;
- pasar listas a texto ordenado cuando proceda;
- usar minusculas para tags;
- mantener acentos y caracteres originales.

