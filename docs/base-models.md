# Auditoría de modelos semilla

Estado: preselección documental, no aprobación de uso. 2026-11-18.

| Candidato | Evidencia primaria | Implicancias |
|---|---|---|
| [Pleias 350M](https://huggingface.co/PleIAs/Pleias-350m-Preview) | Apache-2.0 declarada; desde cero, Common Corpus | Smoke test; no exigir calidad final. |
| [Pleias 1.2B](https://huggingface.co/PleIAs/Pleias-1.2b-Preview) | 1.21B, arquitectura tipo Llama/GPT-Neox, desde cero; español; receta YAML, ~5T tokens procesados; GGUF publicado; autores recomiendan full fine-tuning antes que LoRA | Favorito provisional. Auditar snapshot exacto de datos y código, alcance de la declaración de uso malicioso junto a Apache-2.0, calidad Base/Instruct y exportación propia. |
| [Apertus v1.1 1.5B](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B) | Apache-2.0 declarada; 1.5B compute / 2.0B storage, embeddings no atados, xIELU, destilación de Apertus 8B, 1.7T tokens; variante [Instruct](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B-Instruct) | Alternativa principal; auditar profesor, reconstrucción de datos y condiciones; probar compatibilidad real del runtime y memoria. |
| [HPLT Spanish 2B](https://huggingface.co/HPLT/hplt-2.0-spa_Latn-llama-2b-100bt) | Apache-2.0 declarada, español, preentrenamiento propio sobre corpus web | Candidato condicionado a trazabilidad y derechos heredados. |
| [Pleias 3B](https://huggingface.co/PleIAs/Pleias-3b-Preview) | Misma familia, escala mayor | Alternativa si los pequeños no alcanzan utilidad; medir coste antes de expandir. |
| [OLMo](https://allenai.org/olmo), [Pythia](https://github.com/EleutherAI/pythia) | Referencias de transparencia y checkpoints | Considerar para ciencia y controles; auditar español y datos. |
| [Comma v0.1](https://huggingface.co/common-pile) | 7B, inglés, corpus abierto Common Pile | Escalamiento posterior; no candidato principal al MVP. |

Una arquitectura tipo Llama no implica utilizar pesos de Meta. Una licencia permisiva de pesos tampoco demuestra apertura integral. Aplicar [OSAID 1.0](https://opensource.org/ai/open-source-ai-definition) y nuestros criterios adicionales de procedencia.

## Gates de selección

- Identificar repos, commits, hashes de pesos, arquitectura/config real, tokenizer, código y datos heredados (incluidos maestros y post-training); revisar términos y obligaciones. No afirmar cumplimiento OSI sin evidencia.
- Cargar en Transformers, verificar generación Base en español, pérdidas y tareas objetivas; registrar fertilidad del tokenizer, contexto, memoria y velocidad.
- Verificar exportación y equivalencia GGUF, CPU y hardware local. No confundir un GGUF preexistente con conversión del modelo derivado.
- Evaluar capacidad conversacional con SFT piloto común, misma cantidad de ejemplos, coste comparable y validación independiente. No comparar Base como si fuera Instruct.
- Realizar piloto CPT equivalente con 1–2M tokens, métricas de desarrollo y condiciones equiparadas dentro de cada semilla. Sprint de selección limitado a dos candidatos finalistas; otros solo si fallan.
- Seleccionar con matriz predefinida: español 25%, seguimiento de instrucciones y adaptabilidad 20%, aprendizaje regional 20%, apertura adicional 15%, coste 10%, compatibilidad local 10%. Licencia, trazabilidad mínima y runtime son excluyentes. Normalizar métricas y congelar pesos antes de correr; sin puntuaciones inventadas.

Si no hay semilla elegible con utilidad aceptable y presupuesto confirmado, detener y revisar alcance, no relajar apertura silenciosamente. Ver [plan](mvp-plan.md).

## Segunda pasada de auditoría — fuentes primarias

| Alternativa | Evidencia | Decisión |
|---|---|---|
| [Salamandra 2B](https://huggingface.co/BSC-LT/salamandra-2b) | Documenta mezcla multilingüe y fuentes: Colossal OSCAR 53,05%, StarCoder 13,67%, FineWeb-Edu 10,24%; énfasis en lenguas españolas | Reserva y referencia de capacidad; web accesible no equivale a licencias permisivas por documento. |
| [SmolLM3 3B Base](https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base) | 11T tokens procesados, español como idioma prioritario, [checkpoints intermedios](https://huggingface.co/HuggingFaceTB/SmolLM3-3B-checkpoints), [resumen de transparencia](https://hfmlsoc-smollm3-eu-data-transparency.hf.space/) | Reserva de mayor capacidad potencial; requiere revisión de derechos de corpus web y datos sintéticos, no asumir cumplimiento de política Amalia. |

Pleias declara exclusión de CommonCrawl, transformación sintética de pasajes y tres etapas de entrenamiento (1,6T filtrado ligero; 1,086T filtrado/enriquecido; repetición del segundo). El Common Corpus actual de 2,27T no equivale al snapshot de entrenamiento ni documenta por sí solo orden, filtrado y textos reescritos. La model card contiene una prohibición explícita de uso malicioso; falta determinar su relación jurídica con Apache-2.0, no considerar resuelto. [Ficha](https://huggingface.co/PleIAs/Pleias-1.2b-Preview).

Apertus 1.5B declara destilación desde Apertus-8B-2509 sobre 1,7T tokens de la fase 5, ponderación 90% KL/10% entropía cruzada; evaluar genealogía del profesor y disponibilidad de recetas, datos y términos. [Ficha](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B). El candidato presenta una ruta a cuantizaciones, pero aún no se verificó conversión local del derivado. No se equipara su coste de entrenamiento a un modelo denso 1.5B convencional.

### Secuencia de selección acotada

1. Auditoría documental de Pleias y Apertus (snapshot, LICENSE, card, código, datos, restricciones, genealogía y cambios de corpus): una ficha de decisión por candidato. Si ambos fallan, abrir reserva explícita.
2. Evaluación Base en español con mismo conjunto dev y scoring por candidato, reportar perplejidad solo dentro del mismo tokenizer; tareas con piso de azar y medición de RAM/VRAM/contexto/velocidad. Usar Instruct existente únicamente como referencia descriptiva, no como prueba equivalente de SFT.
3. Después de aprobar plan y datos piloto, comparar adaptación CPT y SFT bajo presupuesto acotado. Si calidad insuficiente en ambos, testear una sola alternativa 2–3B previo recálculo de coste. No ampliar simultáneamente el número de modelos y las dosis.
4. Congelar semilla por revisión/hash y documentar criterio de aprobación de capacidad. No confundir mayor tasa de aciertos con causalidad de adaptación regional.

No se han medido modelos. Las tarjetas y publicaciones no permiten asignar una puntuación empírica.

## Evidencia observada y configuración fija

Ver [prueba de factibilidad](feasibility.md): configs, revisiones candidatas exactas y tamaños anunciados. Apertus presenta discrepancia entre tamaño de parámetros declarado y archivo BF16; no cerrar R02 hasta reconciliar. Se recuperaron ambos tokenizadores por SHA y se midieron cinco frases; falta una evaluación de fertilidad representativa. Mantener candidatos provisoriamente.

## Medición de checkpoint y tokenización

[Corrida local M00](../evidence/M00-feasibility-20261119T031736Z.json): 1.195.468.800 y 1.510.019.136 elementos almacenados respectivamente; no equivalen automáticamente a parámetros entrenables (buffers). La cifra nominal de 2B storage indicada previamente para Apertus no coincide con este checkpoint exacto. Estimación de estados a 18 bytes/elemento: 21,52 y 27,18 GB, antes de activaciones y overhead; confirmar instanciación y entrenamiento antes de presupuestar. Apertus tokenizó 70 frente a 78 tokens de Pleias en cinco frases del script. Esto favorece reevaluar Apertus, no elegirlo sin benchmark, runtime y auditoría heredada.

## Comparación en documentos reales

[Lote SEDICI 001](../evidence/sedici-pilot-001-20261119.json): Pleias 42.097 tokens, Apertus 41.355, diferencia descriptiva de 1,76% a favor de Apertus. En el artículo sobre Sarmiento, Pleias usa 23.816 frente a 23.970 tokens. La ventaja de 10,3% observada en cinco frases no se reproduce con igual magnitud aquí. Tres documentos dirigidos, pendientes de calidad de extracción (advertencias CFF Type1); no establecer superioridad general ni elegir semilla por esta métrica.
