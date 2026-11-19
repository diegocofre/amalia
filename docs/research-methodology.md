# Metodología de investigación reproducible

Amalia trabaja con evidencia versionada desde la etapa fundacional. El objetivo es que una persona o agente independiente pueda reconstruir cada decisión y repetir cada procedimiento, dentro de las restricciones legales y técnicas.

## Ciclo de investigación

1. Formular pregunta, hipótesis, fuente, alcance, criterio de evidencia y límites de recursos.
2. Estudiar fuentes primarias, registrar enlaces y revisiones exactas; separar lo declarado, lo observado y lo inferido.
3. Preparar y versionar scripts, comandos, configuración y dependencias. Revisar y probar sin red las funciones puras cuando corresponda. Fijar versiones antes de ejecución relevante.
4. Ejecutar con límites de volumen, coste, tiempo y permisos; registrar tanto éxitos como fallos. Si no es posible desde el entorno del agente, entregar al operador un comando reproducible contra el commit exacto.
5. Recibir, revisar y versionar evidencia compartible o su manifiesto. Conservar registros de exclusión, errores, cambios de configuración y limitaciones. No reemplazar silenciosamente resultados previos.
6. Resolver hallazgos con evidencia, actualizar decisiones y plan; solicitar revisión independiente cuando aplique. No presentar hipótesis o proyecciones como mediciones.

## Estructura mínima

- `tools/`: scripts exploratorios reutilizables, Python o sh según necesidad.
- `tests/`: pruebas de herramientas y pipeline.
- `docs/`: diseño, antecedentes, protocolos, referencias, decisiones y hallazgos.
- `evidence/`: resultados pequeños revisados y manifiestos de artefactos externos. Cada corrida tiene identificador y registro de procedencia.
- Configuraciones y dependencias se versionan junto a sus consumidores; no crear infraestructura extra antes de necesitarla.

## Evidencia por corrida

Registrar como mínimo ID, fecha UTC, Git SHA y estado limpio/sucio, versión/hash del script, dependencias efectivas, comando y parámetros, versiones y URLs de entradas, hashes disponibles, resultados, errores y limitaciones. En experimentos ML añadir semilla, hardware, presupuesto, métricas y checkpoints. Si un campo no se pudo verificar, declararlo. Para revisar un artefacto externo, conservar ubicación autorizada y hash sin filtrar tokens de acceso.

El Git SHA identifica el procedimiento, no congela una API mutable: conservar la revisión de la fuente, fecha y evidencia material permitida. No considerar registros de licencia como autorización automática. No publicar datos personales, credenciales, archivos restringidos ni contenido no autorizado. Pesos, corpus grandes y logs voluminosos permanecen en almacenamiento apropiado con manifiestos en Git.

## Revisión y avance

El trabajo se hace por incrementos pequeños, con protocolo, evidencia y decisiones enlazadas. El agente propone y la autoridad de control aprueba el alcance. El resultado negativo es evidencia válida. Toda revisión informa las pruebas realmente ejecutadas y los bloqueantes restantes. Los gates se cierran por resultados verificables, no por una opinión del agente. El plan MVP y el registro de revisiones siguen siendo la autoridad para el experimento específico.

Ejemplo inicial: [prueba M00](feasibility.md), [script](../tools/feasibility_probe.py) y [registro de revisiones](mvp-reviews.md).
