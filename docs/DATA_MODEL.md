# Modelo de datos

## Entidad principal: entry

Cada entrada representa un evento, idea, conversacion, decision, tarea, recuerdo, aprendizaje, observacion o nota.

## Campos

| Campo | Tipo | Obligatorio | Descripcion |
| --- | --- | --- | --- |
| `id` | string | si | Identificador unico estable. |
| `schema_version` | integer | si | Version del esquema de importacion. |
| `created_at` | datetime | si | Momento en que se genero el registro. |
| `event_date` | date | si | Fecha del evento. |
| `event_time` | time/null | no | Hora del evento si se conoce. |
| `title` | string | si | Titulo breve. |
| `body` | text | si | Version redactada y legible. |
| `summary` | text | si | Resumen de una o dos frases. |
| `type` | string | si | Tipo principal de registro. |
| `scopes` | string[] | si | Ambitos de vida o contexto. |
| `tags` | string[] | si | Etiquetas breves. |
| `people` | string[] | si | Personas mencionadas. |
| `places` | string[] | si | Lugares mencionados. |
| `projects` | string[] | si | Proyectos o iniciativas. |
| `mood` | string/null | no | Estado emocional. |
| `importance` | integer | si | Relevancia de 1 a 5. |
| `follow_ups` | string[] | si | Acciones posteriores. |
| `source` | object | si | Origen del registro. |
| `raw_input` | text | si | Transcripcion fiel ligeramente limpiada. |
| `cleanup_level` | string | si | Nivel de limpieza aplicado. |
| `content_hash` | string | si | Huella del contenido para detectar duplicados. |
| `processing_notes` | string[] | si | Notas sobre incertidumbres o decisiones de procesamiento. |

## Tipos recomendados

- `event`
- `conversation`
- `idea`
- `decision`
- `task`
- `reflection`
- `learning`
- `health`
- `work`
- `personal`
- `finance`
- `relationship`
- `memory`
- `observation`
- `note`

## Regla de duplicados

- `id` es clave unica.
- Si llega un `id` existente con mismo contenido, se ignora.
- Si llega un `id` existente con contenido distinto, se marca conflicto.
- Si llega un `content_hash` existente con otro `id`, se marca posible duplicado.

