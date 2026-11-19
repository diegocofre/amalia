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
