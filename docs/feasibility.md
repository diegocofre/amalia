# Factibilidad M00 — evidencia y prueba acotada

2026-11-19. Evidencia documental de lectura web; no se ejecutaron modelos ni se descargaron tokenizadores o corpora. Se registran resultados positivos y límites de acceso para evitar convertir evidencia de disponibilidad en volumen probado.

## Semillas

Revisiones de repositorio observadas: [Pleias 6556074d10a57b04bdd46c8a34c97bca67f830ab](https://huggingface.co/PleIAs/Pleias-1.2b-Preview/commit/6556074d10a57b04bdd46c8a34c97bca67f830ab) y [Apertus dbe8919b2f0389888bada6b3a19e81e0ef4286c1](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B/commit/dbe8919b2f0389888bada6b3a19e81e0ef4286c1). Configuraciones leídas en main; lectura web directa del config por SHA no funcionó. Verificar bytes y hashes contra esos SHA antes de utilizar cualquier artefacto.

| Campo | [Pleias config](https://huggingface.co/PleIAs/Pleias-1.2b-Preview/blob/main/config.json) | [Apertus config](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B/blob/main/config.json) |
|---|---:|---:|
| Clase | LlamaForCausalLM | ApertusForCausalLM |
| Capas | 22 | 16 |
| Hidden size | 2048 | 2048 |
| MLP | 6144 | 12288 |
| Cabezas Q/KV | 32/8 | 32/8 |
| Vocabulario | 65536 | 131072 |
| Contexto configurado | 2048 | 4096 |
| Activación | SiLU | xIELU |
| Embeddings atados | sí | no |
| Versión Transformers declarada | 4.46.0 | 4.57.6 |
| Archivo de pesos BF16 anunciado | 2.39 GB | 3.02 GB |
| tokenizer.json anunciado | 4.67 MB | 17.1 MB |

[Apertus model card](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B) dice 1.5B compute / 2.0B storage, pero [árbol de archivos](https://huggingface.co/swiss-ai/Apertus-v1.1-1.5B/tree/main) anuncia 3.02 GB de Safetensors BF16. No resolver por suposición: contar parámetros reales desde metadata del checkpoint y reconciliar con implementación antes de fijar VRAM. Pleias sigue favorito provisional por simplicidad, no por rendimiento medido. No extrapolar calidad de modelos por vocabulario o contexto.

## Muestra documental SEDICI

Muestra dirigida de seis ítems localizados por búsqueda, no aleatoria ni representativa. Licencias declaradas en ficha, enlaces a PDFs indicados; no se descargaron los archivos ni se verificaron excepciones/titularidad. Sin admisión al corpus.

| Registro | Tema | Licencia declarada | Filtro preliminar |
|---|---|---|---|
| [10915/133857](https://sedici.unlp.edu.ar/handle/10915/133857) | Proyectos históricos y valores (1960) | CC BY 4.0 | Revisar derechos y edición histórica |
| [10915/165604](https://sedici.unlp.edu.ar/handle/10915/165604) | Compartiendo conocimiento (2023) | CC BY 4.0 | Candidato |
| [10915/162286](https://sedici.unlp.edu.ar/handle/10915/162286) | Sarmiento y Museo de La Plata (2023) | CC BY 4.0 | Candidato; verificar imágenes/terceros |
| [10915/169483](https://sedici.unlp.edu.ar/handle/10915/169483) | Formación en educación física UNLP (2022) | CC BY 4.0 | Candidato |
| [10915/169156](https://sedici.unlp.edu.ar/handle/10915/169156) | Homenaje a Luis Pazos | CC BY-NC-SA 4.0 | Excluir cadena pública |
| [10915/195059](https://sedici.unlp.edu.ar/handle/10915/195059) | Inclusión financiera argentina (2026) | CC BY-NC-ND 4.0 | Excluir cadena pública |

Resultado: 4/6 con declaración CC BY 4.0 y 2/6 con NC; cero documentos aprobados. No usar 4/6 para inferir proporción del repositorio. La [FAQ de SEDICI](https://sedici.unlp.edu.ar/pages/FAQ) distingue la licencia de distribución no exclusiva al repositorio de la licencia de uso público y contempla embargos. El catálogo observado varía según la fecha de indexación: no extrapolar de distintos totales.

El endpoint OAI-PMH /oai/snrd?verb=Identify no fue accesible vía navegador de investigación; /xoai/snrd?verb=ListRecords&metadataPrefix=oai_dc devolvió HTTP 400 en la consulta. Esto no demuestra caída del servicio. [SNRD](https://repositoriosdigitales.sicyt.gob.ar/) es ruta alternativa de discovery, pero la fuente original sigue siendo necesaria para derechos. [Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus) confirma metadatos de licencia, idioma, colección, identificador y creador, pero no se obtuvo muestra argentina ni conteo.

## Prueba reproducible local (propuesta, pendiente de ejecución)

Desde raíz del repo, Python 3.12 y conexión pública:

```bash
python -m pip install -r tools/requirements-feasibility.txt
python -m unittest discover -s tests -v
python tools/feasibility_probe.py > feasibility-local.json
```

El script no descarga pesos ni documentos, no usa credenciales ni acepta condiciones de datasets. Descarga configs y tokenizer JSON fijados por SHA (límite 24 MiB por respuesta), mide tokenización de frases originales de prueba y consulta hasta dos páginas de metadatos OAI. No es muestra probabilística. Los conteos de frases no representan tokens del corpus. Salida local: JSON con hashes, versiones, parámetros declarados, incidencias y conteos de derechos explícitos. No publicar ciegamente logs ni metadatos privados. Si una fuente falla, las restantes conservan su resultado; repetir con endpoint oficial verificado o buscar alternativa. El script es exploratorio y todavía no fue ejecutado aquí.

Próximo gate: validar acceso, revisar referencias y conseguir una muestra de textos explícitamente aprobados; luego extraer texto y medir tokens útiles con el tokenizer elegido. No calcular proyecciones sin denominador conocido y muestreo apropiado. No pasar a CPT ni declarar elegibilidad por el éxito del script.

## Ampliación v0.2 del probe

Además consulta metadatos públicos de seis datasets, intenta rutas alternativas de SEDICI, registra Git SHA, hash del script y versiones, e inspecciona exclusivamente encabezados Safetensors por HTTP Range (rechaza respuesta 200 sin leer el cuerpo del checkpoint). Los elementos almacenados incluyen buffers y no equivalen automáticamente a parámetros activos. No obtiene filas de corpus ni acepta condiciones gated. Registra hasta 50 handles públicos de SEDICI y enlaces de licencia declarados por endpoint, sin copiar el resto de los metadatos. Registra versiones instaladas (nombres y versiones, no rutas). Las respuestas están acotadas por tamaño y timeout por solicitud; los fallos quedan en el JSON. Dependencia directa fijada, dependencias transitivas efectivas deben registrarse antes de corridas confirmatorias. Pruebas unitarias añadidas, pendientes de ejecución local. Revisar el JSON antes de versionar evidencias según [metodología](research-methodology.md).

## Primera ejecución local — 2026-11-19

[Evidencia M00](../evidence/M00-feasibility-20261119T031736Z.json): commit bf7e803 limpio, Python 3.13.5, tokenizers 0.22.2; 3/3 tests exitosos. El operador recuperó configs, hashes y encabezados fijados por SHA de ambos modelos. Pleias: 1.195.468.800 elementos BF16, 2.390.937.600 bytes de payload; Apertus: 1.510.019.136 elementos, 3.020.038.272 bytes. Tokenización de cinco frases del script: 78 vs 70 tokens (Apertus 10,26% menos); muestra dirigida, no evidencia de calidad lingüística general. SEDICI /xoai/snrd respondió dos páginas, 200 registros únicos: 40 candidatos BY/CC0, 153 NC/ND, 7 desconocidos. Se conservaron 24 handles candidatos del subconjunto expuesto por el probe; no se admitieron documentos. No extrapolar proporciones. Las seis fichas Hub respondieron, sin descargar datos. El JSON versionado es una extracción del log, no el archivo original intacto (acentos alterados al copiar); no incluye mantenimiento de VM ajeno al proyecto. Próximo paso: lote pequeño de documentos autorizados, revisión de derechos y extracción local. No entrenar todavía.

## Primer lote documental: SEDICI 001

[Manifiesto](../configs/sedici-pilot.json) y [script](../tools/ingest_sedici.py). Tres publicaciones dirigidas, CC BY 4.0 declarada en registros y, en dos artículos, primera página del PDF. Revisión de adquisición local para investigación, no dictamen jurídico ni admisión al entrenamiento. Las figuras de terceros no se extraen; el artículo sobre Sarmiento se limita a sus primeras 32 páginas, sin anexos. Los textos conservan citas y pueden contener datos de contacto u otros contenidos pendientes de revisión; se filtran emails como precaución parcial y se inspecciona el texto antes de admitirlo. No redistribuir originales ni textos por esta prueba.

Desde la raíz, con el venv existente:

```bash
python -m pip install -r tools/requirements-corpus.txt
python -m unittest discover -s tests -v
python -m tools.ingest_sedici
```

El comando recupera como máximo el lote explícito (tres documentos, 24 MiB por respuesta), descarga tokenizadores fijados si faltan, conserva PDF por ID, extrae texto UTF-8 por hash y produce JSON en consola y `workspace/runs/`. `workspace/raw/sedici/` y `workspace/processed/sedici/` permanecen entre ejecuciones; tras una segunda corrida deben mantenerse hashes y no repetirse descargas. El campo `cached_pdf` permite comprobarlo. El fichero `workspace/corpus/sedici.jsonl` se reconstruye a partir de aprobaciones por hash y permanece vacío hasta revisión. No es un snapshot ni debe usarse si el reporte tiene errores. La segunda corrida vuelve a calcular extracción y métricas con los mismos originales. Sin OCR, no se fuerza la recuperación de escaneos.

Enviar solo los JSON de las dos corridas y resultados de tests; revisar los textos localmente. Aprobar posteriores hashes específicos mediante modificación revisada del manifiesto (reviewer, review_date, rights_and_privacy_notes, raw_sha256, text_sha256, approved=true). Si se necesita excluir citas o corregir extracción, versionar la transformación antes de aprobar. La redistribución continúa separada y desactivada. No se ha ejecutado este nuevo script desde el agente; esperar evidencia real antes de cerrar R15.

## Resultado local del lote SEDICI 001

[Dos corridas y evidencia comparada](../evidence/sedici-pilot-001-20261119.json), commit 2de2e78 limpio: 8/8 tests, 3 PDF (5.598.056 bytes), 55 de 60 páginas seleccionadas, ninguna página vacía, 144.106 caracteres, 147.362 bytes UTF-8, tres coincidencias de email redactadas. Pleias 42.097 tokens, Apertus 41.355. En los registros de documentos, ambas ejecuciones solo difieren en cached_pdf, de falso a verdadero; hashes, conteos, estados y salida elegible coinciden. Los tres documentos siguen pendientes; corpus elegible vacío. El log contiene 50 advertencias de decodificación CFF Type1 por ausencia de fontTools, no errores de ejecución. No equivale a extracción fiel: próxima prueba, fijar la dependencia fontTools, repetir desde caché, comparar hashes y métricas e inspeccionar textos contra los originales. Preservar esta línea de base y no admitir automáticamente. No se han inspeccionado los PDF/textos locales desde el agente.

## Reextracción y calidad (R16)

Se fija [fonttools 4.66.1](https://pypi.org/project/fonttools/4.66.1/) para decodificación CFF Type1, compatible con Python 3.13 según los requisitos publicados. No se modifica la normalización ni se autoriza admisión. La salida registra versión de fonttools, advertencias pypdf por documento (incluidas otras advertencias), caracteres de reemplazo Unicode, de uso privado y controles inesperados. Estos indicadores son diagnósticos, no una prueba de fidelidad ni de ausencia de datos personales.

```bash
python -m pip install -r tools/requirements-corpus.txt
python -m unittest discover -s tests -v
python -m tools.ingest_sedici --baseline evidence/sedici-pilot-001-20261119.json
```

Reutilizar el workspace; los textos previos se conservan por hash. Comparar los tres originales, hashes de tokenizadores, hashes de texto, diferencias de caracteres y tokens; comprobar que cached_pdf=true y que no quedan avisos CFF. Revisar localmente el texto completo frente a los originales, en especial acentos, signos, orden de lectura, citas y terceros, y datos personales. No aprobar por ausencia de advertencias. Para cualquier admisión registrar decisión y revisión del texto exacto por hash. No compartir PDFs/textos sin revisión. Pruebas nuevas y ejecución real pendientes.
