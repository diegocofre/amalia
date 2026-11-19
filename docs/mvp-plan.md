# Amalia 0.1 — Protocolo técnico del MVP

Versión del plan: 0.2, borrador para revisión. Fecha: 2026-11-18. No autoriza por sí mismo contratación de infraestructura ni entrenamiento confirmatorio. Este documento desarrolla F01–F03 del [roadmap general](../ROADMAP.md); las etapas M00–M07 son subfases del MVP y no reemplazan la numeración general.

## Objetivo y producto

Investigar si la exposición deliberada a patrimonio argentino modifica capacidades regionales de una semilla abierta, comparada con exposición equivalente a español general. En paralelo, entregar una Research Preview pública: modelo Base y derivado Instruct, pesos descargables y GGUF, inferencia local, corpus redistribuible, benchmark, controles y metodología reproducible. No prometer competir con modelos frontier ni utilidad profesional de alto riesgo.

Aplicaciones candidatas a validar: consultas culturales e históricas, educación y divulgación introductoria, resumen y reformulación de textos argentinos, asistente privado local y base para investigación/desarrolladores. El MVP no requiere RAG; un complemento futuro con fuentes actualizadas no constituirá evidencia sobre los pesos.

## M00–M01: restricciones, semilla y gates

Ver [auditoría](base-models.md), [licencias](licensing.md) y [antecedentes](state-of-the-art.md). Pleias 1.2B favorito provisional, Apertus 1.5B competidor (2B almacenados), Pleias 350M smoke test, HPLT 2B y Pleias 3B reservas. No seleccionar por número nominal de parámetros. Antes de gastar: evaluar español, trazabilidad/licencias, calidad conversacional potencial, memoria y conversión local. Congelar una semilla y su hash antes del confirmatorio.

## M02: corpus y diseño experimental

[Inventario y protocolo de admisión](data-sources.md). Objetivo exploratorio principal: 35M tokens argentinos + 15M replay elegible, 35M español general + los mismos 15M replay. Medir tokens únicos/efectivos por separado; no garantizar disponibilidad todavía. Piloto hasta 1–2M tokens por corrida; laboratorio hasta 10M antes de escalar. Objetivo de mezcla regional: 20% historia/geografía/sociedad, 20% ciencia, 20% literatura, 15% educación, 15% instituciones/vida cotidiana, 10% lengua regional. Cuotas orientativas, ajustar por evidencia de disponibilidad y reportar desvíos geográficos, temporales y discursivos.

| Brazo | Tratamiento |
|---|---|
| A | Semilla intacta |
| B | CPT español general + replay |
| C | CPT corpus argentino + replay |

B y C: mismos pesos iniciales, tokenizer, tokens no padding, optimiser, LR/schedule, contexto, batch, pasos, régimen de packing/máscara, hardware comparable y semillas pareadas (42 y 123 propuestas). Igualar géneros, longitud, calidad, época y dificultad tanto como se pueda; declarar diferencias residuales. El efecto identifica el tratamiento compuesto del corpus seleccionado, no una esencia cultural universal. No variar prompts ni usar herramientas para evaluación causal.

Preparar dev y test antes de entrenamiento. Deduplicar corpus entre brazos y evaluación por hash, MinHash y revisión semántica; agrupar por fuente/documento/entidad/autor. Reportar solapamiento conocido con datos originales y contaminación no observable. Separar preguntas que prueban hechos expuestos de generalización con evidencia reservada. Ningún benchmark se usa para entrenamiento.

## M03–M04: laboratorio y piloto

Stack mínimo: Python, PyTorch, Transformers, Datasets, PyArrow/DuckDB, Accelerate, TRL, lm-evaluation-harness, pytest; Git, JSONL y TensorBoard. No MLOps distribuido inicialmente. Fijar versiones y configuración. Smoke test ~100k tokens, Pleias 350M si elegible: descarga, tokenización, entrenamiento, checkpoint/reanudación, evaluación y exportación. Piloto 1–2M por corrida para estabilidad, throughput real, VRAM, LR y selección. Validar batch efectivo y límites de memoria; evaluar sensibilidad de dose antes de decidir si 50M es razonable.

Configuración CPT tentativa para 1.21B: full-parameter causal LM, BF16, AdamW, LR 2e-5 (explorar 1e-5 a 5e-5), cosine, warmup 3%, contexto 2048 si compatible, batch efectivo 65.536 tokens (aprox. 763 updates para 50M; medir tokens válidos y pasos exactos), clip 1, gradient checkpointing. No cambiar tokenizer. Registrar secuencias, packing, máscara documental, seeds, precisión, optimizer y checkpoints. Selección exclusivamente con dev; congelar hiperparámetros antes de test confirmatorio.

## M05: confirmatorio

Dos semillas por brazo entrenado, 4 corridas de 50M tokens si supera gate de factibilidad; checkpoints/evaluación de desarrollo a 5M y 20M, guardar cada 5M según espacio. No mirar test para decidir detener, cambiar datos o hiperparámetros. Stop de seguridad técnica por NaN, divergencia, violación de derechos, memoria o cap de gasto; documentar desviaciones y replanificar, no seleccionar corridas favorables.

Métrica primaria provisional: exactitud pareada en tareas regionales objetivas previamente congeladas, C vs B; definir algoritmo de scoring, conjunto y ponderación antes de entrenamiento. Amalia Bench: 200 casos piloto de desarrollo, objetivo hasta 600 casos confirmatorios independientes (historia/cultura 150, relaciones/generalización 120, pragmática 100, ciencia/educación 100, diversidad territorial 80, incertidumbre 50; ajustar según potencia y curaduría). Si no se consiguen muestras suficientes, reducir afirmaciones y tratar como exploratorio. CHOCLO, Trueque, Belebele, XNLI y GSM8K como referencias secundarias con protocolos fijados; no promediar sin especificar escalas. Base: log-likelihood, opciones y completado; perplejidad solo comparable con tokenizer común. Instruct: ejecución generativa controlada, exactitud, abstención, calidad y evaluación humana ciega con rúbrica/acuerdo.

Objetivos provisionales: +5 pp C vs B en métrica objetiva primaria, efecto positivo en ambas semillas y IC 95% favorable (bootstrap pareado agrupado por entidades/fuentes; distinguir incertidumbre de preguntas de variabilidad entre seeds, dos seeds no bastan para inferencia robusta sobre entrenamiento). No regresión objetivo >3 pp en pruebas generales predefinidas; cuantización <=2 pp de pérdida objetivo. Estudiar potencia con discordancia pareada y agrupación, antes del confirmatorio. Definir no inferioridad con intervalos, no solo diferencia puntual. No afirmar cumplimiento por no detectar significación. Reportar multiplicidad e incertidumbre, todas las corridas, resultados negativos y desviaciones. Interpretabilidad mecanicista exploratoria, no gate. Métricas y umbrales definitivos requieren aprobación en M00/piloto.

## M06: Instruct y distribución

Aplicar SFT equivalente a A/B/C (mismos ejemplos, orden/semillas y receta; decidir de antemano si se repiten todas las semillas o subconjunto preseleccionado y justificar). 10–20k ejemplos objetivo, 1–2 épocas tentativas, máscara de pérdida sobre respuestas, dev independiente, datos humanos auditados. No imponer una personalidad argentina. MessIRve queda fuera de cadena pública salvo resolución de derechos. DPO/RLHF fuera del MVP. Comparar variantes con mismo template y decoding; revalidar seguridad, exactitud y abstención.

Formato Safetensors/BF16 y GGUF Q4/Q8 si compatible. Estimaciones de pesos 1.21B: ~2.42 GB BF16, ~0.8 GB Q4 y ~1.3 GB Q8; medir memoria total y contexto. Objetivo: CPU con 8 GB RAM, 16 GB holgado; verificar cold start, tokens/s, RSS, tiempos de generación y calidad. Transformers y llama.cpp primero; Ollama/LM Studio si compatibles. Publicar instrucciones realmente probadas, no comandos de registros inexistentes.

## Infraestructura y cap

Una GPU alquilada de 48 GB preferida para 1.21B, 80 GB si candidato requiere. Estimación conservadora de estado de entrenamiento 18 bytes/parámetro sin activaciones: ~21.8 GB para 1.21B, ~36 GB para 2B almacenados. Medir VRAM real, optimizer, batch, almacenamiento de checkpoints y recuperación. Para 4 x 50M x 1.21B, aproximación 6ND = 1.45 EFLOP; a 2.000 tokens/s (supuesto) ~27.8 GPU-h, a 500 tokens/s ~111 GPU-h, sin overhead. Medir y cotizar antes de contratar.

Reserva de planificación USD 300: 30 smoke/selección, 100 CPT, 50 SFT/evaluación, 30 almacenamiento/transferencia, 90 contingencia. No es cotización ni incluye horas humanas, asesoría legal u operación permanente. Si throughput o tarifas no permiten completar el diseño con el cap, recalcular y pedir aprobación de nuevo antes de escalar. Apagar instancias ociosas, limitar disco/egreso y registrar consumo. No exigir simultáneamente mantener todos los checkpoints en disco local: política de retención y almacenamiento verificado.

## M07: publicación

Publicar Base, Instruct, controles y checkpoints necesarios, GGUF probado, corpus redistribuible y manifiestos, resultados de evaluación, scripts/configs fijados, logs y coste, data/model cards y reporte técnico. GitHub para código, Hugging Face para artefactos pesados. Demo Gradio/HF Spaces si coste/compatibilidad lo permiten; alternativa local empaquetada y resultados estáticos. Chat y comparación ciega voluntaria C vs B con igual decoding, consentimiento antes de guardar interacciones; feedback separado del test. No anunciar mejoras no observadas. Si licencia o calidad bloquean distribución, publicar informe y artefactos elegibles sin presentar release como exitoso.

## Fases y estimación inicial

| Fase | Gate | Horas humanas orientativas |
|---|---|---:|
| M00 Revisión | protocolo aprobado, bloqueantes resueltos o gates explícitos | 12–20 |
| M01 Semilla | elegibilidad y candidata seleccionada tras pruebas | 8–12 |
| M02 Datos/bench | corpus factible, splits y protocolo congelados | 35–70 |
| M03 Laboratorio | circuito reproducible | 16–24 |
| M04 Piloto | estabilidad, coste y escalabilidad medidos | 8–12 |
| M05 CPT | todas las corridas y análisis | 8–16 |
| M06 Instruct | calidad y runtime medidos | 12–20 |
| M07 Publicación | revisión legal, técnica y artefactos | 12–20 |

Total 111–194 h, horizonte orientativo 4–8 semanas con dedicación suficiente; curaduría de 600 casos y auditoría de derechos podrían exceder sustancialmente la estimación. No fijar fecha de release. Mantener evaluación propia mínima útil y ampliar según potencia/recursos, sin sacrificar congelamiento. Los pasos M01–M04 pueden iterar; selección preliminar no es confirmatoria.

## Registro y revisión

ID de corrida, Git SHA, hashes, versiones, fuentes/criterios de admisión, configuración completa, tokenizer/seed, orden de datos, ambiente y hardware, pérdidas, métricas, VRAM, tiempo/coste, checkpoints y desviaciones. Revisiones independientes de investigación, datos, entrenamiento, apertura, producto y red team. [Registro de hallazgos](mvp-reviews.md). Aprobar plan 1.0 antes de implementación; gates experimentales posteriores se resuelven con evidencia, sin consulta al test congelado. La revisión por LLM no sustituye verificación empírica ni asesoramiento especializado.

## Aclaración tras segunda auditoría documental

La selección conserva dos finalistas provisionales. Salamandra 2B y SmolLM3 3B son reservas condicionadas a apertura y presupuesto; no se amplía el número de entrenamientos principales. Ver secuencia de selección en [semillas](base-models.md). La ruta preferida de corpus comienza por metadatos SEDICI/Common Corpus, datos estructurados y originales identificados en LatamGPT; no presupone convenio ni acceso bajo NDA. Ver prueba de factibilidad en [datos](data-sources.md). Requerir inicialmente cobertura de varias familias documentales humanas y separar verbalizaciones/sintéticos; límites propuestos a validar en piloto. Ningún gate de datos, coste o elegibilidad de modelo se considera cerrado por esta revisión.

## Evidencia M00 adicional

[Factibilidad](feasibility.md) registra configuración de finalistas, muestra documental y prueba local acotada propuesta. No cambia la condición de borrador 0.2; el plan 0.3 requiere resultados empíricos y/o revisión crítica explícita de los gates pendientes. No hay autorización de entrenamiento.

## Laboratorio ejecutable y adquisición acumulativa

El MVP adopta la [metodología de compendio de investigación ejecutable](research-methodology.md). M00 conserva el probe de solo lectura como descubrimiento; M02/M03 deben producir un corpus real local, elegible y persistente por lotes, con catálogo, linaje y reportes generados. Antes de ampliar nuevas fuentes, validar un adaptador piloto con límites, reanudación, idempotencia, admisión y snapshot. Los datos de prueba se separan de entrenamiento y redistribución exige gate independiente. No alterar dosis ni protocolo confirmatorio por un reporte sin revisión y aprobación. Esta precisión no autoriza aún descargar textos masivos ni entrenar.
