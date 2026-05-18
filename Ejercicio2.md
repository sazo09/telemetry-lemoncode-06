# Explica que son los exporters, recording rules y alert rules en el contexto de Prometheus

## Exporters

Los Exporters actúan como "traductores" o agentes: recogen los datos del sistema (ej. uso de disco, conexiones a la DB) y los convierten al formato de texto que Prometheus puede entender.

## Recording Rules

Imagina que tienes una query de PromQL muy compleja que calcula la media de CPU de 100 nodos en los últimos 5 minutos. Si tu dashboard de Grafana pide esa query cada vez que se refresca, estarás estresando al servidor de Prometheus innecesariamente.

Las Recording Rules pre-calculan ese resultado y lo guardan como una nueva métrica ya lista para ser consultada rápidamente.

## Alert Rules

Un ingeniero no puede estar mirando gráficas 24/7. Necesitamos que el sistema nos avise de forma proactiva. Las Alert Rules definen condiciones (ej. "si la CPU es > 90% durante más de 5 minutos") que, al cumplirse, disparan una notificación hacia el Alertmanager.

---

## Arquitectura de Configuración: Estructura Conceptual

En tu entorno de Ubuntu Server, no configurarás esto directamente en el binario, sino a través de archivos YAML que Prometheus leerá al arrancar.

### Exporters (como el Node Exporter)

Generalmente corren como contenedores independientes al lado de Prometheus. En tu configuración, simplemente añadirás una nueva sección de `static_configs` con la IP y el puerto del exporter (ej: `9100` para Node Exporter).

### Reglas (Recording & Alerting)

- Se definen en archivos separados (ej: `prometheus.rules.yml`).
- En el archivo principal `prometheus.yml`, debes indicarle a Prometheus dónde están esos archivos bajo la sección `rule_files`.

### Estructura de una Regla

Se organizan por grupos (`groups`). Cada regla tiene:

- Un nombre (`record` para las de grabación).
- La expresión de PromQL (`expr`) que debe ejecutar.
- En el caso de las alertas, etiquetas y anotaciones para describir el problema.
