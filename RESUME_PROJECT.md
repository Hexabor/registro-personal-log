# Retomar este proyecto con cualquier agente

Usa este archivo como contexto inicial en Codex, Claude Code u otro agente de
desarrollo. Puedes adjuntarlo o pedir al agente que lo lea desde la raiz del
repositorio.

## Encargo para el agente

Retoma el proyecto desde su estado real actual y continua la siguiente tarea
pendiente. No dependas del historial privado de chats anteriores ni pidas al usuario
que reconstruya ese contexto.

Antes de proponer o modificar codigo:

1. Localiza la raiz del repositorio, que contiene `AGENTS.md`.
2. Lee `AGENTS.md` completo y cumple sus protocolos de inicio, trabajo y cierre.
3. Lee las instrucciones especificas de tu herramienta si existen, por ejemplo
   `CLAUDE.md`.
4. Lee `docs/HANDOFF_TO_NEW_CODEX_CHAT.md`, empezando por `CHECKPOINT ACTUAL`. Ese
   bloque define el punto de reanudacion y prevalece sobre la historia posterior del
   documento.
5. Lee `README.md` y los documentos que el checkpoint indique para la siguiente
   tarea.
6. Comprueba el estado real con:

   ```powershell
   git fetch origin
   git status -sb
   git log -3 --oneline --decorate
   git rev-list --left-right --count main...origin/main
   ```

7. Si la copia local esta atrasada, sincronizala de forma segura antes de editar,
   siguiendo `README.md`. Si hay cambios locales no reconocidos, no los borres ni
   los sobrescribas: deten el trabajo y explica el conflicto.
8. En un ordenador nuevo, instala las dependencias de forma reproducible si aun no
   estan disponibles:

   ```powershell
   pnpm install --frozen-lockfile
   ```

9. Ejecuta `pnpm run verify` para validar el punto de partida.
10. Antes de editar, explica al usuario en lenguaje claro:
    - que fases estan terminadas;
    - cual es la siguiente tarea exacta;
    - si Git y las pruebas permiten continuar;
    - cualquier contradiccion o bloqueo encontrado.

## Reglas de continuidad

- El repositorio Git es la fuente de verdad compartida.
- `docs/HANDOFF_TO_NEW_CODEX_CHAT.md` es la fuente de verdad sobre el estado y la
  siguiente tarea.
- No repitas trabajo que el checkpoint marque como terminado.
- No introduzcas fases, tecnologias o decisiones que el checkpoint aun no haya
  abierto.
- Conserva los cambios ajenos y no uses operaciones destructivas de Git.
- Trabaja con el usuario como product owner: explica resultado, coste, riesgo,
  mantenimiento y reversibilidad sin convertir la conversacion en un curso de
  programacion.
- Antes de terminar, aplica el cierre obligatorio de `AGENTS.md`: actualiza el
  checkpoint si corresponde, ejecuta `pnpm run verify`, revisa el diff y publica el
  bloque cuando se haya acordado compartirlo.

## Punto orientativo al crear este archivo

El `2026-07-21`, la fase 0 estaba cerrada y el siguiente bloque previsto era iniciar
la fase 1 con los esquemas Zod, tipos TypeScript y pruebas del contrato JSONL. Esta
nota solo ayuda a detectar errores: confirma siempre el estado vigente en el
`CHECKPOINT ACTUAL` y en Git antes de actuar.

