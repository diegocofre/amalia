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
