# Especificacion del producto

## Vision

Crear una app privada de diario/log personal que permita guardar registros relevantes del dia a dia, consultarlos facilmente y exportarlos sin depender de una plataforma cerrada.

## Usuario principal

Una persona que quiere registrar informacion personal, profesional y practica de forma rapida, especialmente mediante dictado en movil.

## Problema

Los diarios libres son agradables de escribir pero dificiles de buscar. Las bases de datos estructuradas son potentes pero incomodas de alimentar.

Este proyecto combina ambas cosas:

- captura natural mediante chat;
- almacenamiento estructurado;
- busqueda y exportacion fiables.

## Principios

- Capturar debe ser facil.
- Importar debe ser seguro e idempotente.
- Buscar debe ser rapido.
- Exportar debe ser siempre posible.
- El usuario debe conservar sus datos.
- La IA ayuda a estructurar, pero la app valida.

## Modo de uso inicial

El usuario dicta o escribe entradas en un chat con instrucciones compatibles. El chat genera un archivo JSONL. La app importa ese archivo y guarda solo entradas nuevas.

## MVP

La primera version deberia incluir:

- importador JSONL;
- validacion de esquema;
- deteccion de duplicados por `id`;
- deteccion de posibles duplicados por `content_hash`;
- base de datos;
- listado por fecha;
- busqueda textual;
- filtros basicos;
- exportacion CSV;
- exportacion Markdown;
- exportacion JSON.

## Decisiones abiertas

- Stack tecnico de la app.
- Alojamiento local, self-hosted o servicio gestionado.
- Nivel de cifrado en reposo.
- Busqueda semantica con embeddings.
- Adjuntos: imagenes, audios, documentos.

