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
