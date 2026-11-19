# Registro de revisión del MVP

Plan 0.2, revisión documental inicial 2026-11-18. No se han ejecutado entrenamientos ni descargado corpora completos. No se ha realizado revisión independiente de frontera. Los hallazgos siguientes requieren resolución documentada; no representar propuesta como evidencia.

| ID | Severidad | Hallazgo | Tratamiento / evidencia de cierre | Estado |
|---|---|---|---|---|
| R01 | Bloqueante release | Apache-2.0 de Pleias y declaración de uso malicioso; datos exactos de semilla no reconstruidos | Revisar LICENCE/terms, receta, commit, corpus; pedir aclaración si corresponde | Abierto |
| R02 | Importante | Apertus 1.5B computacional, 2B almacenados y destilación | Corregido en estimación; auditar profesor y runtime | Parcial |
| R03 | Bloqueante datos | LatamGPT agregado con condiciones de acceso y sin URL original en esquema | Revisar términos y mapear origen; preferir fuente primaria; medir elegibles | Abierto |
| R04 | Bloqueante release | MessIRve CC BY-NC | Fuera de cadena pública, permiso explícito o análisis jurídico antes de cambiar; no trasladar automáticamente licencia a pesos | Mitigado por alcance |
| R05 | Bloqueante CPT | 35M tokens argentinos elegibles no comprobados | Muestreo, conteo y control comparable; ajustar dosis antes de congelar | Abierto |
| R06 | Bloqueante confirmatorio | Umbrales 5/3 pp y 600 casos no validados estadísticamente | Definir métrica primaria, potencia, agrupación y análisis preespecificado; reconocer límites de dos seeds | Abierto |
| R07 | Importante | 50M tokens puede ser insuficiente para efecto o calidad | Piloto con dev, criterio de escalamiento y posibilidad de resultado nulo | Abierto |
| R08 | Bloqueante gasto | Throughput, VRAM, tarifas y almacenamiento estimados | Prueba medida y presupuesto actualizado | Abierto |
| R09 | Bloqueante release | Compatibilidad GGUF y utilidad conversacional no demostradas | Piloto SFT, conversión propia, medición CPU/RAM y benchmark | Abierto |
| R10 | Importante | 600 casos propios, derechos y diversidad pueden exceder calendario | Medir velocidad de curaduría, estimar recursos y revisar alcance | Abierto |
| R11 | Importante | Roadmap general y fases MVP podrían confundirse | M00–M07 como subfases; enlace y precedencia documental | Resuelto documentalmente |
| R12 | Importante | Sesgo por datos digitalizados y contaminación heredada | Reportar cobertura, limitaciones, agrupación y auditoría; no inferir representatividad sociológica | Abierto |

## Revisiones independientes propuestas

Entregar el commit exacto del plan, bibliografía, inventario, criterios y registro al reviewer. Pedir: identificar supuestos no verificados, refutar hipótesis, citar fuentes primarias, cuantificar impacto, proponer cambio mínimo y criterio de cierre. Clasificar bloqueante/importante/menor. Distinguir bloqueantes del diseño antes de implementación de gates que solo pueden resolverse midiendo durante ejecución.

Perfiles: ML Research (causalidad, métricas y potencia), Data (licencias, muestreo y contaminación), Training (arquitectura, memoria, estabilidad y costes), Open Source (genealogía y permisos), Product (utilidad y distribución local), Red Team (contradicciones, fragilidad, afirmaciones injustificadas). No requerir seis modelos distintos: pueden ser revisiones independientes con instrucciones separadas.

Cada revisión debe registrar ID, fecha, modelo/versión o investigador, commit revisado, hallazgo, evidencia, severidad, decisión razonada y verificación. No cerrar hallazgos sin evidencia, no sustituir revisión jurídica ni experimentos. Mantener plan 0.x hasta aprobar; no iniciar entrenamiento principal con gates abiertos.

## Segunda pasada documental

- R01 sigue abierto: la ficha Pleias implica filtros y reescrituras sintéticas y el snapshot actual no acredita el corpus exacto. Revisar texto jurídico y reconstrucción.
- R02 sigue parcial: identificado objetivo de destilación y maestro; falta auditoría de maestro y runtime.
- R03 sigue abierto: catálogo LatamGPT disponible, PDF supera límite de consulta y dashboard dinámico no permite comprobar filas. Research tiene NDA y afiliación, excluido de ruta pública. No se aceptaron condiciones en nombre del proyecto.
- R05 sigue abierto: SEDICI ofrece ruta OAI-PMH y dos ejemplos con licencia explícita; falta muestreo, extracción y conteo. Wikidata y Datos Argentina complementan pero no sustituyen patrimonio humano.
- R09 sigue abierto: añadidas Salamandra y SmolLM3 como reservas condicionadas; no se han probado ni puntuado.
- R13 (importante): distinguir fuentes humanas, verbalización determinística y reescritura sintética (también heredada de semilla). Evidencia de cierre: etiquetas de procedencia, límites de mezcla, análisis de cobertura y controles de contaminación. Abierto.

Esta pasada no constituye auditoría exhaustiva ni aprobación de candidato o datos. Próxima evidencia: fichas de genealogía con revisión fija, extracción de catálogo y muestreo de metadatos públicos (sin entrenar). Revisar con modelo de frontera antes de aprobar implementación.

## Tercera pasada: evidencia y límites

- R01/R02: revisiones exactas identificadas y configuración main leída; falta verificación por SHA, genealogía y hashes. Nuevo desajuste Apertus entre tamaño anunciado de tensor y parámetros declarados, mantener abierto.
- R05: cuatro fichas con CC BY 4.0, dos NC; muestra dirigida, cero admitidos. Consulta OAI inaccesible/HTTP 400, no inferir caída del servicio ni disponibilidad global. Sigue abierto.
- R14 (importante): la prueba documental no permite medir fertilidad ni volumen. [Prueba acotada](feasibility.md) y script exploratorio propuestos; no ejecutados en el entorno de investigación. Cierre: resultados reales, hashes y muestra aprobada, no meramente existencia del script.

## Metodología y probe ampliado

R14: ampliado script para metadatos Hub, encabezados Safetensors y endpoints alternativos; declara commit/hash y errores. Añadidas pruebas unitarias y dependencia directa fijada. Pendiente ejecución local, no cerrar hallazgo. Se establece [metodología de investigación reproducible](research-methodology.md) para humanos y agentes; versionar cada paso y evidencia revisada.

## Metodología de laboratorio ejecutable

R15 (importante, abierto): el probe actual no produce corpus. Se definió el contrato de adquisición incremental, datos locales, reporte y snapshot, así como metodología cuantitativa/cualitativa y bibliografía. Cierre de implementación: primer adaptador autorizado con lote real local, linaje, reporte, pruebas de idempotencia, reanudación, exclusión y reproducción; no cerrar por existencia de documentación. Se mantiene gate de derechos R05 y ejecución pendiente R14. La decisión tecnológica de orquestación queda condicionada a necesidad medida.

## Síntesis metodológica KISS

Se reducen las instrucciones operativas a un ciclo único; la bibliografía permanece en el estado del arte. Se conserva el criterio de cierre R15 (corpus real local, trazabilidad, reporte, exclusión, reanudación y no duplicación). No se exige CLI, jerarquía de directorios ni orquestador antes de demostrar necesidad. No cambia el protocolo experimental ni el estado de los gates.

## Primera ejecución local M00

3/3 tests válidos; [evidencia](../evidence/M00-feasibility-20261119T031736Z.json). R02: discrepancia de tamaño del archivo resuelta para el SHA inspeccionado (1,510B elementos), queda auditoría de parámetros entrenables, maestro y runtime. R05: acceso SEDICI verificado y 40/200 candidatos declarados; volumen elegible desconocido, abierto. R14: ejecución y hashes acreditados, falta muestra textual aprobada y fertilidad sobre corpus, parcial. R15: pendiente primer lote real. R01, R03 y R09 no se cierran por metadatos. No se cambia semilla ni protocolo confirmatorio.
