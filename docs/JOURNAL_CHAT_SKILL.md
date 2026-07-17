# Skill: Registro personal estructurado compatible con importador

## Proposito

Convierte mensajes dictados o escritos por el usuario en registros estructurados, exportables e importables por una app de diario/log personal.

El objetivo es que el usuario pueda hablar de forma natural y que el asistente genere entradas consistentes, con identificadores unicos, campos normalizados y formato estable.

Este documento debe funcionar como contrato de compatibilidad entre el chat de captura y la app que importara los registros.

## Principios generales

- Mantener siempre el texto original del usuario en `raw_input`.
- `raw_input` debe ser una transcripcion fiel ligeramente limpiada, no una transcripcion literal con todo el ruido del dictado.
- Crear una entrada separada por cada evento, idea, conversacion, decision, tarea, recuerdo u observacion relevante.
- No inventar datos sensibles ni detalles que el usuario no haya dicho.
- Si un dato es incierto, usar `null`, una lista vacia o anadir una nota en `processing_notes`.
- Priorizar compatibilidad y consistencia sobre creatividad.
- Usar siempre el mismo esquema de salida.
- Generar IDs unicos para evitar duplicidades al importar.
- Incluir un `batch_id` comun para todas las entradas generadas en una misma sesion o volcado.
- No repetir entradas ya generadas dentro del mismo lote.

## Formato recomendado de salida

El formato principal debe ser JSONL: un objeto JSON valido por linea.

No envolver la salida JSONL en una lista.
No anadir comentarios dentro del JSONL.
No usar Markdown dentro del bloque JSONL salvo que el usuario lo pida expresamente.

Ejemplo:

```jsonl
{"id":"evt_20260717_184233_8f3a9c","schema_version":1,"created_at":"2026-07-17T18:42:33+02:00","event_date":"2026-07-17","event_time":"18:42","title":"Conversacion sobre el viaje","body":"He hablado con Marta sobre el presupuesto del viaje.","summary":"Conversacion con Marta sobre presupuesto del viaje.","type":"conversation","scopes":["personal","travel"],"tags":["viaje","presupuesto"],"people":["Marta"],"places":[],"projects":[],"mood":"tranquilo","importance":3,"follow_ups":["Mirar vuelos esta semana"],"source":{"kind":"ai_chat","batch_id":"batch_20260717_1842","assistant":"unspecified"},"raw_input":"Hoy he hablado con Marta sobre el presupuesto del viaje. Hemos decidido mirar vuelos esta semana. Me senti bastante tranquilo.","content_hash":"sha256:pending","processing_notes":[]}
```

## Esquema obligatorio

Cada registro debe incluir estos campos:

```json
{
  "id": "string",
  "schema_version": 1,
  "created_at": "ISO-8601 datetime with timezone",
  "event_date": "YYYY-MM-DD",
  "event_time": "HH:MM or null",
  "title": "string",
  "body": "string",
  "summary": "string",
  "type": "string",
  "scopes": ["string"],
  "tags": ["string"],
  "people": ["string"],
  "places": ["string"],
  "projects": ["string"],
  "mood": "string or null",
  "importance": 1,
  "follow_ups": ["string"],
  "source": {
    "kind": "string",
    "batch_id": "string",
    "assistant": "string"
  },
  "raw_input": "string",
  "cleanup_level": "none | light | medium | heavy",
  "content_hash": "string",
  "processing_notes": ["string"]
}
```

## Reglas de identificacion

Cada entrada necesita un `id` unico y estable.

Formato recomendado:

```text
evt_YYYYMMDD_HHMMSS_xxxxxx
```

Donde:

- `evt` es el prefijo fijo.
- `YYYYMMDD` es la fecha de creacion del registro.
- `HHMMSS` es la hora de creacion del registro.
- `xxxxxx` es un sufijo aleatorio o pseudoaleatorio de 6 caracteres hexadecimales.

Ejemplo:

```text
evt_20260717_184233_8f3a9c
```

Si el asistente no puede generar aleatoriedad real, debe crear un sufijo suficientemente variable usando una combinacion de numero secuencial, contenido y hora.

Nunca reutilizar el mismo `id` para dos registros distintos.

## Reglas de `batch_id`

Todas las entradas creadas en una misma respuesta deben compartir el mismo `batch_id`.

Formato recomendado:

```text
batch_YYYYMMDD_HHMM
```

Ejemplo:

```text
batch_20260717_1842
```

Si se generan varios volcados en la misma hora y minuto, anadir sufijo:

```text
batch_20260717_1842_02
```

## `content_hash`

El campo `content_hash` sirve para detectar posibles duplicados por contenido.

Si el asistente puede calcular SHA-256, debe calcularlo sobre esta concatenacion normalizada:

```text
event_date|title|body|type|people|tags
```

Si no puede calcular SHA-256 con fiabilidad, debe usar:

```text
sha256:pending
```

La app importadora podra recalcularlo.

## Fechas y horas

Usar siempre fechas absolutas.

Si el usuario dice "hoy", convertirlo a la fecha actual conocida por el chat.

Si el usuario dice "ayer", convertirlo a la fecha absoluta correspondiente.

Si la fecha no esta clara:

- `event_date`: usar la mejor inferencia disponible.
- anadir una nota en `processing_notes`.

Si la hora del evento no esta clara:

- `event_time`: `null`.

`created_at` representa el momento en que se genera el registro, no necesariamente el momento del evento.

## Tipos permitidos

Usar preferentemente uno de estos valores para `type`:

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

Si hay duda, usar `note`.

## Ambitos o `scopes`

`scopes` describe las areas de vida o contexto.

Valores recomendados:

- `personal`
- `work`
- `family`
- `friends`
- `health`
- `finance`
- `home`
- `travel`
- `learning`
- `creative`
- `admin`
- `relationship`
- `project`

Puede haber varios scopes.

## Tags

Los `tags` deben ser breves, en minusculas y sin almohadilla.

Ejemplos:

- `viaje`
- `presupuesto`
- `ansiedad`
- `reunion`
- `idea-app`
- `seguimiento`

No crear demasiados tags. Normalmente entre 2 y 6 por entrada.

## Personas

`people` debe incluir nombres mencionados explicitamente por el usuario.

No inferir identidades.

Si el usuario dice "mi hermano" sin nombre, usar `"mi hermano"`.

Si hay varias personas, incluirlas todas.

## Lugares

`places` debe incluir lugares concretos mencionados.

Ejemplos:

- `Madrid`
- `casa`
- `oficina`
- `consulta medica`

## Proyectos

`projects` debe incluir proyectos, iniciativas o frentes de trabajo mencionados.

Ejemplos:

- `diario personal`
- `mudanza`
- `viaje a Japon`
- `app de registros`

## Estado emocional

`mood` debe ser una palabra o frase breve.

Ejemplos:

- `tranquilo`
- `nervioso`
- `ilusionado`
- `cansado`
- `confuso`

Si no se menciona ni se puede inferir con prudencia, usar `null`.

## Importancia

`importance` debe ser un numero entero de 1 a 5.

Guia:

- 1: detalle menor o nota casual.
- 2: registro util pero poco relevante.
- 3: relevancia normal.
- 4: importante, con impacto claro.
- 5: muy importante, sensible, decisivo o de alto impacto.

Si hay duda, usar 3.

## Seguimientos

`follow_ups` debe contener tareas, compromisos o proximas acciones mencionadas.

Ejemplo:

```json
"follow_ups": ["Enviar presupuesto a Marta", "Revisar vuelos esta semana"]
```

Si no hay seguimientos, usar lista vacia.

## Titulo

`title` debe ser breve, especifico y humano.

Bueno:

```text
Conversacion con Marta sobre vuelos
```

Malo:

```text
Registro importante
```

## Resumen

`summary` debe condensar la entrada en una o dos frases.

No debe contener informacion que no este en `body` o `raw_input`.

## Cuerpo

`body` debe ser una version limpia y redactada de lo dicho por el usuario.

Debe conservar el significado original.

Puede corregir muletillas, repeticiones y errores claros de dictado.

No debe convertir una entrada personal en un texto frio o excesivamente formal.

## Entrada original

`raw_input` debe conservar fielmente, en la medida de lo posible, el texto dictado o escrito por el usuario, pero puede limpiarse de ruido evidente de dictado.

Por defecto, usar `cleanup_level: "light"`.

Se puede corregir en `raw_input`:

- muletillas que no aportan significado, como `eh`, `mmm`, `bueno` o `a ver`;
- repeticiones accidentales;
- falsos arranques y autocorrecciones claras;
- errores obvios de reconocimiento de voz;
- puntuacion, mayusculas y cortes de frase;
- instrucciones de correccion del propio dictado, si queda claro que no forman parte del registro.

No se debe corregir en `raw_input`:

- contenido emocional;
- nivel de certeza o duda;
- contradicciones importantes;
- palabras raras pero intencionadas;
- insultos, ironias o formulaciones personales si expresan algo real;
- detalles sensibles;
- fechas, nombres, cantidades o compromisos, salvo que el error sea clarisimo.

Regla de oro:

```text
Se puede limpiar la forma, pero no cambiar la intencion, la certeza, la emocion ni los hechos.
```

Valores permitidos para `cleanup_level`:

- `none`: literal o casi literal.
- `light`: limpia muletillas, repeticiones y errores obvios.
- `medium`: reorganiza frases sin cambiar significado.
- `heavy`: resumen o reescritura fuerte, solo si el usuario lo pide expresamente.

Si el usuario dicta varias entradas en un bloque, cada registro debe incluir en `raw_input` solo la parte correspondiente a esa entrada.

`body` debe ser mas legible que `raw_input`: puede ordenar frases, suavizar repeticiones y redactar la entrada como texto de diario, sin cambiar el significado.

## Division de entradas

Si el usuario habla de varios hechos claramente distintos, crear varios registros.

Ejemplo de mensaje:

```text
Hoy he llamado a mi madre y la he notado mas animada. Tambien se me ocurrio una idea para la app: que pueda exportar por semanas. Y tengo que pedir cita con el dentista.
```

Debe generar tres registros:

- una entrada de tipo `conversation` o `personal`;
- una entrada de tipo `idea`;
- una entrada de tipo `task`.

## Modo mixto

El sistema trabaja en modo mixto:

- Si la entrada es clara y de bajo riesgo, generar el registro directamente.
- Si la entrada es ambigua, sensible o puede tener consecuencias importantes, generar el registro y anadir una nota en `processing_notes`.
- Si falta un dato imprescindible para guardar correctamente, preguntar antes de generar el archivo.

Datos imprescindibles:

- contenido principal de la entrada;
- fecha del evento, aunque pueda inferirse como hoy.

## Salida para revision humana

Cuando el usuario pida revisar antes de guardar, mostrar primero una tabla breve con:

- titulo;
- fecha;
- tipo;
- ambitos;
- personas;
- importancia.

Despues, si el usuario confirma, generar el JSONL.

## Salida directa para importacion

Cuando el usuario pida "generame el archivo", "preparalo para importar", "exportalo" o similar, responder con:

1. Un nombre de archivo sugerido.
2. Un bloque JSONL valido.
3. Nada mas dentro del bloque.

Ejemplo:

```text
Nombre sugerido: journal_import_20260717_1842.jsonl
```

```jsonl
{"id":"evt_20260717_184233_8f3a9c", ...}
```

## Compatibilidad CSV

Todos los campos principales deben poder convertirse a CSV.

Para campos de lista, la app puede unir valores con `;`.

Ejemplo:

```text
people = "Marta; Carlos"
tags = "viaje; presupuesto"
```

## Compatibilidad Markdown

Cada registro debe poder convertirse a Markdown asi:

```md
## 2026-07-17 - Conversacion sobre el viaje

- ID: evt_20260717_184233_8f3a9c
- Tipo: conversation
- Ambitos: personal, travel
- Personas: Marta
- Tags: viaje, presupuesto
- Importancia: 3

He hablado con Marta sobre el presupuesto del viaje.

Seguimientos:
- Mirar vuelos esta semana
```

## Manejo de duplicados

El asistente debe evitar duplicados dentro de una misma respuesta.

La app importadora debe tratar `id` como clave unica.

Regla recomendada de importacion:

- Si `id` no existe: insertar.
- Si `id` existe y el contenido es igual: ignorar.
- Si `id` existe y el contenido es distinto: marcar conflicto.
- Si `content_hash` ya existe con otro `id`: marcar posible duplicado.

## Privacidad

No resumir ni suavizar datos sensibles hasta perder precision.

No anadir juicios personales.

No incluir diagnosticos medicos, legales o psicologicos salvo que el usuario los haya expresado explicitamente.

Si aparece informacion muy sensible, mantenerla en el registro pero clasificarla con mayor cuidado:

- `importance`: 4 o 5 si procede.
- tags adecuados, por ejemplo `salud`, `legal`, `finanzas`, `conflicto`.

## Ejemplo completo

Entrada del usuario:

```text
Hoy he hablado con Marta sobre el presupuesto del viaje. Hemos decidido mirar vuelos esta semana. Me senti bastante tranquilo. Tambien se me ha ocurrido que la app del diario deberia poder exportar por semanas en Markdown.
```

Salida:

```jsonl
{"id":"evt_20260717_184233_8f3a9c","schema_version":1,"created_at":"2026-07-17T18:42:33+02:00","event_date":"2026-07-17","event_time":null,"title":"Conversacion con Marta sobre el viaje","body":"He hablado con Marta sobre el presupuesto del viaje. Hemos decidido mirar vuelos esta semana. Me senti bastante tranquilo.","summary":"Conversacion con Marta sobre presupuesto del viaje y decision de mirar vuelos esta semana.","type":"conversation","scopes":["personal","travel"],"tags":["viaje","presupuesto","vuelos"],"people":["Marta"],"places":[],"projects":[],"mood":"tranquilo","importance":3,"follow_ups":["Mirar vuelos esta semana"],"source":{"kind":"ai_chat","batch_id":"batch_20260717_1842","assistant":"unspecified"},"raw_input":"Hoy he hablado con Marta sobre el presupuesto del viaje. Hemos decidido mirar vuelos esta semana. Me senti bastante tranquilo.","cleanup_level":"light","content_hash":"sha256:pending","processing_notes":[]}
{"id":"evt_20260717_184234_b91d02","schema_version":1,"created_at":"2026-07-17T18:42:34+02:00","event_date":"2026-07-17","event_time":null,"title":"Exportacion semanal en Markdown","body":"Se me ha ocurrido que la app del diario deberia poder exportar registros por semanas en Markdown.","summary":"Idea para permitir exportaciones semanales en formato Markdown.","type":"idea","scopes":["personal","project"],"tags":["diario","exportacion","markdown"],"people":[],"places":[],"projects":["app de registros"],"mood":null,"importance":3,"follow_ups":[],"source":{"kind":"ai_chat","batch_id":"batch_20260717_1842","assistant":"unspecified"},"raw_input":"Tambien se me ha ocurrido que la app del diario deberia poder exportar por semanas en Markdown.","content_hash":"sha256:pending","processing_notes":[]}
```
