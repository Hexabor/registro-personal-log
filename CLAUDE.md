# Instrucciones para Claude Code

Bienvenido al repositorio `registro-personal-log`.

Al inicio de cada sesion, antes de responder sobre el proyecto o editar cualquier
archivo:

1. Lee completo `AGENTS.md`; sus reglas se aplican a todo el repositorio.
2. Lee primero la seccion `CHECKPOINT ACTUAL` de
   `docs/HANDOFF_TO_NEW_CODEX_CHAT.md` y despues el resto que sea relevante.
3. Revisa que `AGENTS.md`, este archivo y el checkpoint sigan siendo coherentes con
   el repositorio. Actualizalos si se han quedado obsoletos.
4. Ejecuta `git status -sb` y `git log -3 --oneline --decorate`.
5. Explica brevemente al usuario el punto exacto desde el que vas a continuar antes
   de hacer cambios.

Lee `docs/CLAUDE_CODE_WELCOME.md` solo la primera vez que uses este proyecto, cuando
lo abras en un equipo nuevo o si han cambiado la instalacion o el protocolo de
colaboracion. No es una lectura obligatoria en cada sesion normal.

No asumas que el historial de una conversacion externa esta disponible: todo el
contexto valido debe salir del repositorio. Si una instruccion del chat contradice
el checkpoint, pide confirmacion y deja documentada la decision final.

Al final de cada sesion vuelve a revisar `AGENTS.md`, este archivo y el checkpoint.
Actualiza `docs/HANDOFF_TO_NEW_CODEX_CHAT.md` aunque el trabajo haya quedado a medias
si su estado material ha cambiado. Ejecuta `pnpm run verify`, revisa el diff y deja
un commit publicable. Si el usuario ha autorizado publicar el bloque, haz tambien
push y comunica el hash del commit. Si no hubo cambios materiales, confirma que los
documentos siguen siendo exactos sin crear un commit vacio.

La siguiente tarea no se decide desde este archivo: siempre la marca el checkpoint.
