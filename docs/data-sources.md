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

## Segunda pasada: rutas de adquisición concretas

| Prioridad | Fuente y acceso | Evidencia / límite |
|---|---|---|
| 1 | [SEDICI](https://sedici.unlp.edu.ar/) — [política](https://sedici.unlp.edu.ar/pages/politicas), [OAI-PMH anunciado por SNRD](https://biblioteca.sicyt.gob.ar/recursos/SEDICI) (http://sedici.unlp.edu.ar/xoai/snrd) | Portal informa 191.533 recursos al consultar; no es conteo elegible. Licencia por obra. Consultar Identify/ListMetadataFormats/ListRecords, conservar resumptionToken, filtrar metadatos de derechos y texto completo. No descargar PDFs hasta revisión de derechos. |
| 2 | [Wikidata](https://www.wikidata.org/wiki/Wikidata:Data_access/es) — SPARQL y dumps | Datos estructurados CC0; elegir consultas acotadas por propiedad/entidad, no extraer texto de fuentes citadas; registrar QID, propiedades, referencias y revisión. Generar frases mediante plantillas determinísticas marcadas como verbalización de datos, no obra humana. Evitar dominancia y reservar entidades de evaluación. |
| 3 | [Datos Argentina](https://www.datos.gob.ar/) — CKAN | Catálogo de datos públicos abiertos por temas; revisar licencia y recurso concreto. Priorizar conjuntos textuales y documentación humana frente a verbalización masiva de tablas. |
| 4 | [Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus) | Metadatos de idioma, colección, fecha, identificador, licencia, creador y texto; identificador coincide con URL en muchos casos, no todos. No dispone de país confiable declarado; identificar fuente/autor/tema y verificar manualmente. |
| 5 | [Catálogo LatamGPT](https://www.latamgpt.org/gcs/catalogo-referencial.pdf) y [dashboard](https://www.latamgpt.org/dashboard) | Mapa de fuentes y licencias para localizar originales. Catálogo no inspeccionado íntegramente: consulta web rechazó archivo >10MB; dashboard dinámico no expuso filas. No inferir volúmenes de fuentes. |
| En cuarentena | [LatamGPT Research](https://huggingface.co/datasets/latam-gpt/LatamGPT-Corpus-1.0-research) | Acceso académico acreditado, NDA y autorización, ~16,2% de volumen completo conforme a ficha; no es requisito ni fuente de cadena pública. |
| En cuarentena | [UBA Games Corpus](https://ri.conicet.gov.ar/items/238a45c5-ce7c-4ed3-994d-1aff621388e6) | Diálogo espontáneo argentino con anotaciones, CC BY-NC-SA declarada; explorar permiso independiente y consentimiento. |
| Pendiente | [Corpus de Referencia de la Lengua Española en Argentina](https://www.lllf.uam.es/wordpress/recursos/corpus/) | Más de 2M palabras, sitio dice libre uso; obtener licencia explícita y verificar derechos de textos subyacentes, no admitir por esa etiqueta. |

Ejemplos de registros SEDICI con CC BY 4.0 y texto completo declarados (no descargados ni admitidos): [Los proyectos históricos y los valores, 1960](https://sedici.unlp.edu.ar/handle/10915/133857?show=full), [Compartiendo conocimiento, 2023](https://sedici.unlp.edu.ar/handle/10915/165604?show=full). Verificar titularidad, PDF concreto, terceros y privacidad. El acceso OAI-PMH se ha identificado, no probado mediante cosecha en esta revisión.

### Prueba de factibilidad propuesta (después de aprobar alcance)

- Cosecha de metadatos acotada: hasta 1.000 registros por fuente seleccionada, con muestreo estratificado; candidatos CC0/CC BY primero, licencias ambiguas y NC/ND excluidas hasta decisión. Registrar evidencia, URL, fuente y muestreo. Revisión manual de hasta 50 registros por estrato inicial y test de extracción en subconjunto autorizado.
- Medir rendimiento por estrato: N registros, fracción con licencia admisible, acceso real, extracción correcta, fracción argentina con evidencia, deduplicación y mediana/media robusta de tokens útiles. Proyectar volumen solo con tamaño del universo conocido y diseño de muestreo; reportar rango/limitaciones, no extrapolar de ejemplos elegidos por búsqueda.
- Medir cobertura por dominio y región, proporción humana vs verbalizada, tiempo de curaduría y coste. Requerir material de al menos tres familias de fuentes humanas para corpus regional principal; no completar volumen con datos sintéticos. Limitar verbalizaciones a 10% provisional y ninguna fuente dominante por defecto; revisar según evidencia.
- Orden de decisión: 1–2M tokens auditados por brazo para piloto; hasta 10M para primer laboratorio; 35M+35M+15M como objetivo confirmatorio condicionado a factibilidad. No declarar gate de volumen cerrado sin conteo real con tokenizer de semilla y control comparable.
- Si falta corpus, reducir dosis simétricamente y reformular hipótesis/potencia antes de congelar test; no incorporar NC/ND o derechos desconocidos para completar una cuota.

Objetivo de esta inspección: pasar de listas genéricas a mecanismos concretos de adquisición. El volumen públicamente anunciado no es volumen argentino elegible; no existe todavía un conteo medido.

## Muestra dirigida y accesibilidad

Ver [factibilidad](feasibility.md): seis fichas SEDICI (4 CC BY 4.0, 2 NC), cero documentos admitidos. El muestreo no permite extrapolación; acceso OAI confirmado en la ejecución local posterior. No hay medición de tokens elegibles.

## Adquisición como desarrollo del corpus

Toda fuente investigada se registra en el catálogo versionado; cuando es elegible para adquisición se implementa como adaptador incremental con entradas/salidas, límites y manifiesto, conforme a la [metodología de investigación](research-methodology.md). Metadatos, originales permitidos, derivados y corpus elegible son artefactos locales vinculados; el informe mide el estado real del flujo. Revisar cobertura documental y social de los resultados, no inferir representatividad nacional por volumen. Los primeros lotes aprobados permanecen disponibles y no se descargan nuevamente sin razón.

## Resultado de descubrimiento local

[Corrida M00](../evidence/M00-feasibility-20261119T031736Z.json): endpoint /xoai/snrd operativo, 200 registros consecutivos, 40 candidatos BY/CC0 (20%), 153 NC/ND (76,5%), 7 desconocidos (3,5%). No es una muestra probabilística. 24 handles candidatos conservados en la evidencia; falta identificar obra y derechos aplicables antes de adquirir texto. Common Corpus sin licencia global declarada en la API, LatamGPT gated auto con licencias múltiples, MessIRve CC BY-NC, CHOCLO MIT (solo evaluación), OASST1 y Aya Apache-2.0 declaradas. Revisiones y hashes registrados; ninguna licencia de ficha equivale a admisión.
