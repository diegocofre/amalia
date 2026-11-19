# Inventario de fuentes y admisión de datos

Revisión documental inicial: 2026-11-18. Ningún corpus se considera admitido por aparecer aquí. Validar revisión exacta, licencia aplicable, procedencia, privacidad, jurisdicción, calidad y elegibilidad de entrenamiento y redistribución según [política](licensing.md).

## Candidatos CPT y replay

| Fuente | Evidencia y utilidad | Pendiente / condición |
|---|---|---|
| [Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus) | Colecciones culturales, científicas, estatales y web; autores declaran más de 10B tokens en español y metadatos documentales. | Identificar versión usada en semilla, cobertura argentina, fuentes originales, licencia por documento. |
| [LatamGPT Corpus 1.0](https://huggingface.co/datasets/latam-gpt/LatamGPT-Corpus-1.0) | Ficha: 143.402.544 registros, 101 shards, ~384 GB, campos id/text/language/license/country/topic/dataset_name/text_length. | Acceso condicionado; el campo de país es multilabel, no prueba autoría argentina; no hay URL original en el esquema publicado. Recuperar procedencia de cada colección y revisar términos antes de descargar o entrenar. |
| [Common Pile](https://huggingface.co/common-pile) | Fuentes abiertas y scripts de recolección. | Medir español, cobertura y trazabilidad. |
| [Wikidata](https://www.wikidata.org/wiki/Wikidata:Licensing) | Datos estructurados CC0; verbalización determinística y con etiqueta de origen. | Revisar exactitud, fuentes externas y separación de evaluación. |
| [Wikipedia](https://es.wikipedia.org/), [Wikisource](https://es.wikisource.org/), [Gutenberg](https://www.gutenberg.org/) | Referencia, literatura y patrimonio. | CC BY-SA cuando aplique, derechos por obra, edición, traducción, jurisdicción y dominio público pagante argentino. |
| [CONICET Digital](https://ri.conicet.gov.ar/), [SNRD](https://biblioteca.sicyt.gob.ar/recursos/SNRD), [SEDICI](https://sedici.unlp.edu.ar/) | Producción científica y académica; explorar OAI-PMH. | Licencia y permiso por artículo, no por mera disponibilidad. |
| [Datos Argentina](https://datos.gob.ar/), [INTA](https://www.argentina.gob.ar/inta), [InfoLeg](https://www.argentina.gob.ar/normativa) | Información pública, científica e institucional. | Verificar licencia y derechos de terceros, representatividad; limitar dominancia normativa. |
| Biblioteca Nacional, CONABIP, archivos provinciales | Patrimonio y diversidad territorial. | Identificar colecciones digitalizadas y permisos; no depender de convenios para el piloto. |

La cifra de 296,5B tokens comunicada por LatamGPT y sus gráficos de país corresponden al corpus completo, no a la descarga ofrecida. No extrapolar volúmenes argentinos elegibles. La ficha también advierte sobre información personal residual y señales de trazabilidad incorporadas. No eliminar señales de procedencia.

## SFT y recuperación

| Fuente | Uso previsto |
|---|---|
| [OASST1](https://huggingface.co/datasets/OpenAssistant/oasst1) (Apache-2.0 declarada) | Instrucciones humanas en español, seleccionar ramas y calidad; auditar texto/licencias/PII y evitar fuga. |
| [Aya Dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) (Apache-2.0 declarada) | Instrucciones multilingües; auditar anotación, origen, traducciones y subset español. |
| [MessIRve](https://huggingface.co/datasets/spanish-ir/messirve) (CC BY-NC 4.0 declarada) | Consultas reales y pasajes Wikipedia. No usar en cadena pública abierta hasta resolución legal. Posible brazo aislado no comercial, sujeto a revisión; solicitar permiso a autores. Transformar a QA solo con verificación de correspondencia y derechos; el origen geográfico de la consulta no implica tema argentino. |
| [Latam Cities QA](https://huggingface.co/datasets/latam-gpt/latam-cities-qa), [Personas Instruct](https://huggingface.co/datasets/latam-gpt/personas-instruct) | Candidatos sintéticos secundarios, en cuarentena; auditar generación, exactitud, derechos y contaminación. |

## Evaluación exclusivamente

- [CHOCLO](https://huggingface.co/datasets/latam-gpt/CHOCLO): MIT declarado; agrupar por entidad, verificar muestra y categorías. No tratar preguntas relacionadas como independientes.
- [Trueque](https://www.latamgpt.org/en/resources): colaboración cultural; fijar versión y condiciones antes de usar.
- [Belebele](https://huggingface.co/datasets/facebook/belebele), [XNLI](https://huggingface.co/datasets/facebook/xnli), [GSM8K](https://huggingface.co/datasets/openai/gsm8k): comprensión, inferencia y matemática; validar formato, idioma, licencia y sensibilidad a la escala.
- Amalia Bench: conjunto propio, desarrollo y test confirmatorio separados, curaduría documentada.

## Protocolo de factibilidad

1. Registrar fuente y versión inmutable, licencia/evidencia, URL original, autor, región (con evidencia), fecha, género, hash bruto y procesado; restringir acceso si contiene información personal.
2. Inspeccionar muestras estratificadas por colección, dominio, país y licencia. Registrar aceptación, motivos de exclusión, duplicación, calidad y coste de acceso.
3. Medir con tokenizer elegido: tokens únicos elegibles y tokens procesados, antes y después de limpieza. Descargar por lotes acotados; streaming no garantiza bajo egreso si el filtro exige recorrer shards completos.
4. Construir control español comparable y replay elegible idéntico por brazo. Agrupar splits por documento, autor, entidad y fuente; deduplicar entre CPT, SFT y evaluación.
5. Publicar inventario de aceptados, descartados y pendientes, data card, atribuciones y manifiestos; no publicar datos en cuarentena.

Objetivo 35M tokens regionales únicos, 35M de control y 15M replay compartidos; no es una disponibilidad comprobada. Validar primero 1–2M por brazo y hasta 10M para laboratorio. Si el inventario elegible no alcanza, reducir simétricamente el tamaño y revisar protocolo/potencia, o aplazar; nunca rellenar con datos dudosos. Ver [plan](mvp-plan.md).
