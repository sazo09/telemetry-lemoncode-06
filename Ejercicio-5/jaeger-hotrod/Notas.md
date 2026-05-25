# Notas — Ejercicio 5.2: Desafío Jaeger con HotROD

## Configuración del entorno

- Jaeger All-in-One: `jaegertracing/all-in-one:latest`
- HotROD Demo App: `jaegertracing/example-hotrod:latest`
- Comunicación entre contenedores vía OTLP HTTP (`http://jaeger:4318`)

---

## Arquitectura de HotROD (observada en el DAG de Jaeger)

HotROD ejecuta 4 microservicios desde un único binario:

```
frontend (:8080)
├── → customer (:8081)  →  MySQL (simulado)
├── → driver   (:8082)  →  Redis (simulado)
└── → route    (:8083)  ×10
```

> **Cómo verlo:** Jaeger UI → Dependencies → pestaña DAG

---

## Issue #1 — Redis Timeouts (errores aleatorios)

**Síntoma observado en Jaeger:**
- Spans de `redis GetDriver` con fondo rosa/rojo
- Tag `error=true` visible al expandir el span
- Log dentro del span: `"redis timeout"`

**Causa raíz:**
El servicio `driver` simula fallos aleatorios de Redis para reproducir
comportamiento real de producción donde las dependencias externas fallan.

**Cómo identificarlo:**
1. Buscar una traza en Jaeger UI → servicio `frontend`
2. Expandir el span `driver` → ver los spans de Redis
3. Hacer clic en un span rosa → Tags: `error=true`
4. Ver Logs del span: mensaje de timeout

**Lección clave:**
Los **tags** (`error=true`) permiten filtrar trazas con errores.
Los **logs** dentro del span dan el detalle del error con timestamp preciso.
Búsqueda por tag en Jaeger: escribir `error=true` en el campo Tags → Find Traces.

---

## Issue #2 — Cuello de botella en MySQL (lock de conexión única)

**Síntoma observado en Jaeger:**
- Con múltiples peticiones simultáneas, el span `mysql` pasa de ~300ms a >1s
- En los logs del span aparece: `"waiting for lock"` con el ID de otras peticiones en cola

**Causa raíz:**
El código simulaba una única conexión a base de datos con un mutex:
```go
// database.go
d.lock.Lock(ctx)   // ← una sola goroutine puede acceder a la vez
defer d.lock.Unlock()
```

**Fix aplicado (en el código fuente de HotROD):**
- Comentar `d.lock.Lock(ctx)` y `d.lock.Unlock()` → simula connection pool correcto
- Reducir `MySQLGetDelay` de 300ms a 100ms

**Lección clave:**
El **baggage** de OpenTracing propaga el `request ID` del cliente JavaScript
a través de todos los microservicios sin pasarlo como parámetro explícito.
Esto permite que el lock muestre qué otras peticiones están esperando.

---

## Issue #3 — Worker pool del servicio route demasiado pequeño

**Síntoma observado en Jaeger:**
- Patrón de "escalera" en los spans de `route`: máximo 3 peticiones en paralelo
- Gaps visibles entre grupos de spans (el frontend espera sin hacer nada)
- El servicio `route` no es el cuello de botella — lo es el frontend al despacharlo

**Causa raíz:**
```go
// config.go
RouteWorkerPoolSize = 3  // ← solo 3 goroutines en el pool
```

**Fix aplicado:**
- Cambiar `RouteWorkerPoolSize` de `3` a `100`
- Resultado: todas las peticiones a `route` se ejecutan en paralelo

**Cómo confirmarlo en Jaeger:**
- Antes del fix: spans de route en grupos de 3, con gaps entre grupos
- Después del fix: todos los spans de route solapados horizontalmente

**Lección clave:**
La vista de timeline de Jaeger hace visible el paralelismo (o su ausencia).
Un patrón de "escalera" siempre indica un pool de workers limitado.

---

## Conceptos clave consolidados

| Concepto | Definición práctica observada |
|----------|-------------------------------|
| **Trace** | El viaje completo de una petición de taxi: desde el click en el UI hasta la respuesta |
| **Span** | Una operación individual: `SQL SELECT`, `redis GET`, `HTTP /route` |
| **Tags** | Metadatos estáticos del span: `error=true`, `http.url`, `sql.query` |
| **Logs** | Eventos con timestamp dentro del span: `"redis timeout"`, `"waiting for lock"` |
| **Scope** | El span activo en el contexto de ejecución actual (goroutine/hilo) |
| **Baggage** | Datos propagados a través de toda la traza sin cambiar las firmas de las funciones |

---

## Comandos utilizados

```bash
# Arrancar el entorno
docker compose up

# Interfaces disponibles
# HotROD UI:  http://localhost:8080
# Jaeger UI:  http://localhost:16686

# Parar el entorno
docker compose down
```
