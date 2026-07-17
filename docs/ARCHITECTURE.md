# Arquitectura de la aplicacion

## Objetivo

La app recibe archivos JSONL generados por ChatGPT, los valida, permite revisar la importacion y mantiene una fuente de datos central accesible desde el Pixel y el ordenador.

## Monorepo

```text
apps/web
  React, TypeScript y Vite

apps/api
  Hono sobre Node.js

packages/contracts
  Esquemas Zod y tipos compartidos
```

## Dependencias permitidas

```text
web -> contracts
api -> contracts
contracts -> Zod
```

La web no conoce la base de datos. La API no contiene componentes de interfaz. Los contratos no dependen de ninguno de los dos.

## Flujo inicial

```text
ChatGPT
-> archivo JSONL
-> web
-> API Hono
-> validacion compartida
-> almacenamiento central pendiente de confirmar
```

## Decisiones abiertas

- Confirmar SQLite como base inicial y su estrategia de migracion a PostgreSQL.
- Elegir alojamiento y almacenamiento persistente.
- Definir autenticacion, cifrado y backups.
- Definir el alcance offline posterior al MVP online-first.

## Regla de migracion

El importador Python se mantiene como referencia hasta que las pruebas demuestren que la implementacion TypeScript conserva su comportamiento. La logica de dominio no dependera de Hono ni de una base de datos concreta.

## Red de desarrollo

La API escucha por defecto solo en `127.0.0.1`. No se debe abrir a la red privada o publica durante el desarrollo. El alojamiento futuro tendra que declarar `API_HOST=0.0.0.0` de forma explicita dentro de su entorno aislado.

## Presentacion y temas

La apariencia no debe quedar acoplada a la logica de producto. La web usara tokens
semanticos mediante variables CSS para color, tipografia, espaciado, radios, sombras
y movimiento. Los componentes consumiran esos tokens en lugar de codificar valores
de una skin concreta.

La primera version solo necesita un tema cuidado y mobile-first. Esta separacion
permitira incorporar mas adelante modo claro/oscuro o skins intercambiables sin
duplicar componentes, validacion, estado ni acceso a datos.
