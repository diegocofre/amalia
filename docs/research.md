# Agenda científica y laboratorio inicial

## Pregunta rectora

¿Hasta qué punto podemos modificar la representación del mundo de un modelo de lenguaje mediante la incorporación deliberada del patrimonio cultural, científico, lingüístico e intelectual de una sociedad?

## Hipótesis y alcance

La exposición adicional a textos culturalmente situados puede modificar asociaciones semánticas, conocimiento, comprensión pragmática y generación. No se presume que surja una identidad, que el modelo experimente emociones ni que supere a modelos generalistas mayores. La característica cultural debe emerger de los datos, no de un prompt estereotipado.

Explorar semiótica y representación, variantes regionales, humor e ironía, conocimiento histórico e institucional, pluralidad, memoria colectiva y efectos de la literatura. El Aleph sirve como analogía conceptual de representación distribuida y expresión sucesiva; no como modelo matemático ni fuente autorizada de entrenamiento.

## Primer experimento

1. Auditar candidatos [Pleias](https://huggingface.co/PleIAs) 350M/1.2B/3B, Comma y OLMo; verificar corpus heredado, licencias, tokenizer, checkpoints y capacidad en español.
2. Elegir una semilla pequeña y congelar su versión y hash. Preparar corpus piloto argentino elegible (objetivo exploratorio 10M tokens o menos) y control universal en español con género, época, calidad y volumen comparables.
3. Separar conjuntos de evaluación por documento, autor o fuente cuando sea viable; controlar contaminación y duplicados.
4. Comparar A: semilla sin cambios; B: entrenamiento general; C: entrenamiento argentino con presupuesto, tokens e hiperparámetros equivalentes. Explorar después mezcla con datos generales para reducir olvido catastrófico. Repetir semillas aleatorias según presupuesto.
5. Medir pérdida en textos reservados, conocimiento local y general, comprensión semántica y pragmática, diversidad dialectal, alucinaciones, calibración y regresiones. Para generación abierta, usar evaluación humana ciega, rúbricas y acuerdo entre evaluadores.
6. Registrar versiones de datos, software, hiperparámetros, hardware, tiempo, costes y checkpoints. Publicar resultados negativos e incertidumbre. Explorar activaciones y representaciones internas con controles adecuados; no interpretarlas como prueba automática de comprensión cultural.

El continual pre-training se evalúa separadamente del SFT conversacional; no confundir mejora por instrucciones con efecto cultural. El RAG puede complementar conocimientos cambiantes pero no sustituye la hipótesis de modificación de pesos.

## Referencias iniciales para auditar

- [Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus)
- [Common Pile](https://github.com/r-three/common-pile)
- [OLMo](https://allenai.org/olmo)
- [Open Source AI Definition](https://opensource.org/ai/open-source-ai-definition)

Las referencias son puntos de partida, no decisiones de selección ni certificaciones de derechos.
