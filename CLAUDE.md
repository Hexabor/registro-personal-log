# Instrucciones para Claude Code

Bienvenido al repositorio `registro-personal-log`.

Antes de responder sobre el proyecto o editar cualquier archivo:

1. Lee completo `AGENTS.md`; sus reglas se aplican a todo el repositorio.
2. Lee primero la seccion `CHECKPOINT ACTUAL` de
   `docs/HANDOFF_TO_NEW_CODEX_CHAT.md` y despues el resto que sea relevante.
3. Lee `docs/CLAUDE_CODE_WELCOME.md` para orientarte, instalar el proyecto y conocer
   el flujo de colaboracion.
4. Ejecuta `git status -sb` y `git log -3 --oneline --decorate`.
5. Explica brevemente al usuario el punto exacto desde el que vas a continuar antes
   de hacer cambios.

No asumas que el historial de una conversacion externa esta disponible: todo el
contexto valido debe salir del repositorio. Si una instruccion del chat contradice
el checkpoint, pide confirmacion y deja documentada la decision final.

Al terminar cualquier bloque relevante debes actualizar
`docs/HANDOFF_TO_NEW_CODEX_CHAT.md`, ejecutar `pnpm run verify`, revisar el diff y
dejar un commit publicable. Si el usuario ha autorizado publicar el bloque, haz
tambien push y comunica el hash del commit.

La siguiente tarea no se decide desde este archivo: siempre la marca el checkpoint.

