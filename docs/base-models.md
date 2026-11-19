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
