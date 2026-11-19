# Antecedentes y estado del arte

Inventario vivo, revisión documental inicial: 2026-11-18. Las descripciones resumen las fuentes enlazadas, no certifican apertura, calidad ni acuerdos de colaboración.

## Modelos regionales y comunidades

| Antecedente | Aporte a Amalia | Fuente |
|---|---|---|
| LatamGPT (CENIA, 2026) | CPT y SFT regional sobre Llama 3.1 70B, infraestructura, corpus y evaluaciones. La genealogía y licencia de Llama limitan una afirmación de apertura integral. | [Recursos e informe técnico](https://www.latamgpt.org/en/resources), [datasets](https://huggingface.co/latam-gpt/datasets) |
| TangoIA (2024) | Adaptación argentina de Llama/Nemotron con una variante de MessIRve; estudiar receta y resultados antes de intentar replicarla. Actividad actual pendiente de confirmar. | [TangoIA](https://tangoia.com/), [pesos](https://huggingface.co/sandbox-ai/Llama-3.1-Tango-70b-bnb_4b) |
| Tucano 2 (2026) | Recetas, ablations y evaluación de modelos pequeños en portugués; distingue entrenamiento desde cero de CPT sobre Qwen. No todas sus variantes tienen la misma genealogía. | [Paper](https://arxiv.org/abs/2603.03543), [receta](https://huggingface.co/blog/Polygl0t/tucano2) |
| Masakhane | Investigación participativa en lenguas africanas; referencia para participación federal. | [Proyecto](https://www.masakhane.io/) |
| SEA-LION / SEA-HELM | Adaptación y evaluación lingüística y cultural regional. | [Proyecto](https://sea-lion.ai/), [evaluación](https://leaderboard.sea-lion.ai/) |
| ALIA / BSC | Infraestructura lingüística e institucional de España. | [Recursos BSC-LT](https://huggingface.co/BSC-LT) |
| Apertus | Apertura de recetas, datos y pesos; modelos destilados compactos. | [Swiss AI](https://www.apertus-ai.org/), [1.5B](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B) |
| Pleias / Common Corpus | Entrenamiento desde cero sobre fuentes declaradas permisivas; candidato a semilla. | [Modelos](https://huggingface.co/collections/PleIAs/common-models), [corpus](https://huggingface.co/datasets/PleIAs/common_corpus) |
| Common Pile / Comma | Corpus abierto de 8 TB y modelos 7B, predominantemente inglés; antecedentes de escala futura. | [Paper](https://arxiv.org/abs/2506.05209), [artefactos](https://huggingface.co/common-pile) |
| SomosNLP | Comunidad de PLN abierto en español y portugués. | [Comunidad](https://somosnlp.org/comunidad) |

## Bibliografía metodológica

- [Pythia, Biderman et al. (2023)](https://proceedings.mlr.press/v202/biderman23a.html): checkpoints y experimentos sobre dinámica de aprendizaje.
- [Don't Stop Pretraining, Gururangan et al. (2020)](https://aclanthology.org/2020.acl-main.740/): adaptación por preentrenamiento adicional; no prueba que nuestra escala sea suficiente.
- [OLMo](https://allenai.org/olmo): transparencia de artefactos y evaluación.
- [CulturalBench](https://arxiv.org/abs/2410.02677): medición de conocimiento cultural.
- [Culturally Aware and Adapted NLP](https://aclanthology.org/2025.tacl-1.31/): taxonomía y problemas de evaluación cultural.
- [MessIRve](https://arxiv.org/abs/2409.05994): recuperación de información en español; consultas y pasajes, no corpus patrimonial ni instrucciones listas para SFT.
- [Open Source AI Definition 1.0](https://opensource.org/ai/open-source-ai-definition): libertades, código, información sobre datos y parámetros. No exige redistribuir todos los datos indiscriminadamente; Amalia aspira además a procedencia por documento y corpus redistribuible.

## Posibles colaboraciones (sin contactos ni acuerdos confirmados)

Priorizar SomosNLP, CENIA/LatamGPT, autores de MessIRve, [LIAA UBA/CONICET](https://www.liaa.dc.uba.ar/), [FAMAF UNC](https://www.famaf.unc.edu.ar/), UNSAM/CELES, [Vía Libre](https://ia.vialibre.org.ar/), [Wikimedia Argentina](https://wikimedia.org.ar/), [Biblioteca Nacional](https://www.bn.gov.ar/), [CONABIP](https://www.conabip.gob.ar/) y [Fundación Sadosky](https://fundacionsadosky.org.ar/) (explorar acceso a Clementina XXI, sin asumir convocatoria abierta). Verificar canales vigentes antes de contactar.

## Posicionamiento e interrogantes

No reivindicar primacía argentina ni latinoamericana. Investigar comparativamente el efecto del patrimonio argentino en una semilla auditable, con controles, distribución local y participación federal. Distinguir conocimiento factual, adecuación pragmática, generalización y evidencia sobre representaciones internas. Aprender de antecedentes sin replicar resultados no documentados.

Actualizar este inventario con referencia primaria, fecha, revisión, evidencia y limitaciones. Para recursos operativos ver [fuentes](data-sources.md), [semillas](base-models.md) y [plan del MVP](mvp-plan.md).

## Antecedentes adicionales

- [SmolLM3](https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base): modelo multilingüe 3B con checkpoints y fuentes documentadas; referencia para capacidad y reproducibilidad, derechos de datos web pendientes.
- [Salamandra 2B](https://huggingface.co/BSC-LT/salamandra-2b): mezcla multilingüe con énfasis en lenguas de España y fuentes publicadas; referencia para adaptación y SFT.
- [LatamGPT catálogo referencial](https://www.latamgpt.org/resources): posible mecanismo de discovery de aportantes por colección; pendiente análisis íntegro.
- [SEDICI](https://sedici.unlp.edu.ar/): ruta de adquisición por metadatos y derechos por recurso, no licencia indiscriminada.

## Antecedentes metodológicos transversales

La [metodología de investigación](research-methodology.md) sintetiza estos antecedentes. Se adoptan sus principios; no constituyen dependencias obligatorias ni certificaciones de cumplimiento.

| Referencia | Principio incorporado |
|---|---|
| Gentleman y Temple Lang, Statistical Analyses and Reproducible Research (2007), recogido en [Research Compendia — The Turing Way](https://book.the-turing-way.org/reproducible-research/compendia/) | Integrar métodos, datos, código y textos en una unidad reproducible y ejecutable. |
| [The Turing Way](https://www.turing.ac.uk/research/research-projects/turing-way) | Ciencia abierta, diseño de investigación, colaboración y ética. |
| Mölder et al., [Sustainable data analysis with Snakemake](https://doi.org/10.12688/f1000research.29032.2) (2021) | Flujos explícitos, regenerables, transparentes y adaptables. |
| [Applying the FAIR Principles to computational workflows](https://doi.org/10.1038/s41597-025-04451-9) (2025) | Diferenciar especificación y ejecución; trazabilidad, metadatos, interoperabilidad, acceso condicionado cuando corresponda. |
| [DVC pipelines](https://doc.dvc.org/user-guide/pipelines/running-pipelines) | Dependencias, hashes y reconstrucción selectiva de resultados; posible herramienta futura. |
| Kandpal et al., [The Common Pile v0.1](https://proceedings.neurips.cc/paper_files/paper/2025/hash/52acc050138d6f40dad6f12f91a4ce22-Abstract-Datasets_and_Benchmarks_Track.html) (2025) | Corpus para LLM con código de adquisición/curaduría, mezcla y checkpoints publicados. |
| Fetters, Curry y Creswell, [Achieving Integration in Mixed Methods Designs](https://doi.org/10.1111/1475-6773.12117) (2013) | Integrar resultados cuantitativos y cualitativos en preguntas, muestreo, colección e interpretación. |
| Bender y Friedman, [Data Statements for NLP](https://aclanthology.org/Q18-1041/) (2018) | Documentar poblaciones, procedencia, contextos lingüísticos y límites de generalización. |
| Sen et al., [A Total Error Framework for Digital Traces](https://doi.org/10.1093/poq/nfab018) (2021) | Distinguir errores de representación y medición de fuentes digitales, sin equiparar disponibilidad con representatividad. |

