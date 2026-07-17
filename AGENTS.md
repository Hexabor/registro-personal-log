# Reglas de trabajo para agentes

Este archivo se aplica a todo el repositorio y es la referencia comun para Codex,
Claude Code y cualquier otro agente de desarrollo.

## Inicio obligatorio de cada sesion

En cada sesion nueva, antes de proponer o modificar codigo:

1. Leer `AGENTS.md` y las instrucciones especificas del agente, como `CLAUDE.md`.
2. Leer `docs/HANDOFF_TO_NEW_CODEX_CHAT.md`, empezando por `CHECKPOINT ACTUAL`.
3. Revisar que esas reglas y el checkpoint siguen siendo coherentes con el estado
   real del repositorio. Corregirlos si se detecta informacion obsoleta.
4. Leer `README.md` y los documentos que el checkpoint indique para la tarea.
5. Ejecutar `git status -sb` y `git log -3 --oneline --decorate`.
6. Confirmar que la rama local no esta atrasada respecto a `origin/main`. Si lo
   esta, detenerse antes de editar y sincronizar de forma segura.
7. No repetir trabajo que el handoff marque como terminado.

`docs/CLAUDE_CODE_WELCOME.md` solo es de lectura obligatoria en el primer uso de
Claude Code en el proyecto, al preparar un equipo nuevo o cuando cambien de forma
relevante el entorno, la instalacion o el flujo de colaboracion.

## Fuente de verdad

- El repositorio Git es la fuente de verdad compartida entre agentes y equipos.
- `docs/HANDOFF_TO_NEW_CODEX_CHAT.md` es la fuente de verdad sobre el punto de
  continuacion, decisiones, pendientes y comprobaciones.
- `docs/PRODUCT_SPEC.md` define el producto.
- `docs/ARCHITECTURE.md` define los limites tecnicos.
- `docs/IMPORT_FORMAT.md` y `docs/DATA_MODEL.md` definen el contrato de datos.
- Ante contradicciones, detenerse, exponerlas al usuario y corregir la
  documentacion cuando se tome una decision.

## Modelo de colaboracion

- El usuario actua como product owner; el agente actua como equipo de desarrollo.
- Explicar decisiones en terminos de coste, resultado, riesgo, mantenimiento y
  reversibilidad. No convertir el trabajo en un curso de programacion salvo que el
  usuario lo pida.
- Hacer supuestos pequenos y reversibles para avanzar. Consultar decisiones de
  producto, privacidad, seguridad, coste o alcance que cambien materialmente el
  resultado.
- No añadir tecnologia por moda ni sustituir decisiones ya aprobadas sin justificar
  el cambio y obtener confirmacion.

## Reglas de implementacion

- Stack aprobado: React + TypeScript + Vite para `apps/web`, Hono sobre Node.js
  para `apps/api` y Zod en `packages/contracts`.
- Respetar las dependencias: `web -> contracts`, `api -> contracts`; la web no
  accede directamente a la base de datos y los contratos no dependen de las apps.
- La captura ocurre en ChatGPT. La app importa, valida, revisa, almacena, consulta y
  exporta JSONL; no crear una captura con IA dentro de la app sin una nueva decision.
- Mantener el producto mobile-first para Pixel 10 y usable tambien en ordenador.
- Separar logica, datos y presentacion. Los estilos nuevos deben usar variables o
  tokens semanticos de tema, de modo que en el futuro puedan existir skins sin
  duplicar componentes ni logica.
- Mantener la API en `127.0.0.1` durante el desarrollo. No exponerla a redes
  publicas o privadas salvo en un entorno de despliegue aislado y deliberado.
- El importador Python es solo una referencia temporal de compatibilidad. La nueva
  implementacion se escribe en TypeScript.
- No introducir SQLite, autenticacion, despliegue, sincronizacion offline o busqueda
  semantica antes de que el checkpoint o el usuario abran esa fase.

## Calidad y seguridad

- Añadir o actualizar pruebas cuando cambie el comportamiento.
- Antes de cerrar un bloque ejecutar `pnpm run verify` desde la raiz.
- No incluir secretos, credenciales, datos personales reales, bases de datos ni
  archivos locales de configuracion en Git.
- No borrar ni reescribir cambios ajenos. Si hay cambios locales no reconocidos,
  detenerse y aclarar su procedencia.
- No usar operaciones destructivas de Git ni forzar un push.

## Git y trabajo desde varios equipos

- Al empezar en un equipo, traer el estado remoto antes de editar.
- Para trabajo individual y secuencial se usa `main`, segun el acuerdo actual.
- Si dos agentes o equipos van a trabajar a la vez, cada tarea debe usar una rama
  corta propia y unirse despues mediante revision; nunca deben editar
  simultaneamente sobre la misma copia o rama.
- Hacer commits pequenos, coherentes y descriptivos. Subirlos al remoto al terminar
  un bloque aprobado para que el trabajo no dependa de un solo ordenador.
- No confirmar ni subir cambios no relacionados sin revisarlos expresamente.

## Cierre obligatorio de cada sesion

Antes de terminar cualquier sesion, incluso si el bloque previsto quedo a medias:

1. Volver a revisar `AGENTS.md`, las instrucciones especificas del agente y la
   seccion `CHECKPOINT ACTUAL` para asegurar que siguen reflejando el modo real de
   trabajo.
2. Actualizar la seccion `CHECKPOINT ACTUAL` de
   `docs/HANDOFF_TO_NEW_CODEX_CHAT.md` con lo realizado, lo pendiente, decisiones,
   bloqueos, pruebas y siguiente tarea exacta. Si no hubo cambios materiales, no es
   necesario crear un commit vacio: basta con comprobar que el checkpoint sigue
   siendo exacto.
3. Actualizar tambien README, arquitectura o especificaciones si dejaron de ser
   exactos.
4. Ejecutar `pnpm run verify` y registrar cualquier comprobacion que no pueda
   completarse.
5. Revisar el diff y comprobar que no contiene secretos ni cambios ajenos.
6. Hacer commit y push cuando el usuario haya pedido publicar o el bloque de trabajo
   se haya acordado como compartido.
7. Confirmar al usuario la rama, el commit publicado, las pruebas y el punto de
   reanudacion.
