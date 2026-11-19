# Instrucciones para agentes de Amalia

Leer primero el README, el [roadmap](ROADMAP.md), la [metodología de investigación reproducible](docs/research-methodology.md) y el plan activo. Mantener alcance pequeño, riguroso y revisable.

## Regla obligatoria: versionar cada paso

- Toda consulta experimental, script Python/shell, prueba de factibilidad, transformación, configuración, evaluación o herramienta usada para producir evidencia del proyecto debe quedar en Git antes de su ejecución reproducible. No depender de comandos perdidos en un chat. Si se ejecutó una exploración manual, registrar comandos, fuente, fecha, resultados y límites en documentación versionada.
- Priorizar herramientas pequeñas, reutilizables y determinísticas. Incluir instrucciones de ejecución, dependencias fijadas, controles de descarga/recursos, errores explícitos y pruebas locales cuando correspondan.
- Cada ejecución registra Git SHA, versión del script/config, hash de entradas cuando sea posible, dependencias, fecha, parámetros, salidas, errores y limitaciones. Registrar resultados nulos y fallidos. No inventar evidencias ni cerrar gates por existencia de un script.
- Evidencia pequeña, revisada y no sensible: versionar en Git con su manifiesto. Corpus, pesos, logs grandes o privados: almacenar fuera de Git según derechos y privacidad, versionar manifiesto, hash, ubicación autorizada y procedimiento de recuperación. No commitear secretos, datos personales innecesarios ni material no redistribuible.
- Si el agente carece de acceso a una fuente, cómputo o entorno, preparar un script acotado, versionarlo y entregar un comando reproducible al operador humano. Integrar las evidencias que devuelva, distinguiendo observación de inferencia.
- Estudiar primero sin alterar el proyecto; presentar plan y obtener aprobación de la autoridad de control (humana o supervisora). Implementar dentro del alcance; revisar diff y pruebas antes de commit, no declarar pruebas ejecutadas si no lo están. Requerir aprobación para gastos, cambios significativos de alcance y merge. Preservar independencia científica y publicar limitaciones.

La metodología se aplica desde la fase de investigación, no solamente al entrenamiento. Ver [metodología completa](docs/research-methodology.md).

## Regla obligatoria: laboratorio ejecutable y corpus acumulativo

- Amalia es un compendio de investigación ejecutable. Una investigación de fuentes debe producir, cuando se autorice, componentes reutilizables del pipeline y datos locales persistentes, además del informe. El probe de metadatos es una fase de descubrimiento, no el corpus.
- Toda fuente tiene un registro versionado, adaptador, límites, permisos de adquisición/entrenamiento/redistribución separados, entradas y salidas explícitas. El flujo local incorpora automáticamente lotes aprobados, sin volver a bajar o duplicar datos ya registrados. Nunca admitir documentos por la mera etiqueta de licencia de un catálogo.
- Separar originales inmutables cuando se permita conservarlos, cuarentena, textos derivados, corpus elegible y releases congeladas; preservar linaje, hashes, motivos de exclusión y revisión de derechos. Una corrección o retiro crea una nueva revisión y marca descendientes afectados; respetar obligaciones de eliminación, privacidad y retención.
- Mantener un informe generado de cobertura, disponibilidad, calidad, tokens por tokenizer, duplicación, idiomas, géneros, territorios y desconocidos. Las métricas deben citar corrida y denominador. El agente analiza la evidencia junto al conocimiento cualitativo y propone cambios de hipótesis, muestra, fuente o protocolo; no reescribe automáticamente conclusiones ni cambia gates confirmatorios.
- Distinguir exploración y confirmación: planes y corpus confirmatorios congelados; revisiones posteriores registradas como nuevas versiones. No usar test reservado para ajustar datos o hiperparámetros. Aplicar métodos cuantitativos y cualitativos según pregunta y respetar límites de generalización.
- Mantener una sola ruta local de ejecución, inicialmente Python y archivos/Parquet; añadir DVC u orquestación cuando haya necesidad demostrada. No lanzar adquisiciones masivas, publicar datos o entrenar fuera de alcance aprobado. Las pruebas deben verificar acumulación idempotente, no fuga de cuarentena y reproducibilidad desde snapshots preservados.
