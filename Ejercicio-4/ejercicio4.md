# Conceptos Basicos de Trazabilidad

## 1. Span
El span es la unidad individual de trabajo dentro de un sistema.

Piensalo como una operacion unica que tiene un inicio y un fin en el tiempo.

Ejemplos:
- Una llamada a base de datos (`SELECT`).
- El renderizado de una pagina.
- Una solicitud HTTP a otro microservicio.

Dato clave: cada span tiene un nombre, una hora de inicio y una duracion especifica.

## 2. Traza (Trace)
Una traza es el recorrido completo de una solicitud a traves de todo el sistema distribuido.

Conceptualmente, es un conjunto de spans organizados de forma jerarquica y temporal.

Visualizacion:
- Suele verse como una traza padre que engloba multiples spans hijos.
- Permite ver el flujo completo desde la accion del usuario hasta la respuesta final.

## 3. Scope
El scope (o alcance) define donde inicia y donde termina cada llamada.

Funcion:
- Delimita el contexto de ejecucion de un span o bloque de codigo.
- Asegura que los datos de telemetria se asocien al momento y lugar correctos.

## 4. Tags
Los tags son pares clave-valor con metadatos adicionales sobre un span.

Uso:
- Sirven para filtrar y consultar trazas en Jaeger.
- Ayudan a indexar y clasificar informacion para detectar problemas rapidamente.

Ejemplos comunes:
- `http.status_code: 200`
- `db.instance: customers`
- `user.id: 12345`