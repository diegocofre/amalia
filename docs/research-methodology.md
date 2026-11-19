# Cómo investigamos en Amalia

Amalia es un laboratorio de investigación ejecutable: código, datos y conocimiento evolucionan juntos. Aplicamos KISS, ciencia abierta y métodos cuantitativos y cualitativos. Los [antecedentes científicos](state-of-the-art.md#antecedentes-metodológicos-transversales) fundamentan este enfoque.

## Un solo ciclo de trabajo

1. **Investigar:** formular una pregunta concreta, consultar fuentes primarias y definir qué evidencia permitiría responderla.
2. **Planificar:** acordar el incremento mínimo, criterios de éxito, permisos y límites de recursos.
3. **Ejecutar:** versionar scripts, configuración y dependencias; probarlos y ejecutarlos localmente. Si el agente no puede, el operador ejecuta el comando contra el commit indicado.
4. **Medir:** conservar datos autorizados y evidencia, incluidos errores y resultados negativos.
5. **Aprender:** interpretar los resultados, revisar hipótesis y actualizar el plan. La autoridad de control aprueba cambios relevantes; los reportes no modifican decisiones automáticamente.

## El corpus se construye trabajando

Cada fuente investigada se registra con su origen, versión y permisos. Cuando se autoriza su adquisición, el script incorpora lotes reales al laboratorio local: descubrir → adquirir → procesar → validar → acumular. Debe poder reanudarse y repetirse sin duplicar datos. Conservar originales autorizados y linaje mediante identificadores y hashes. Separar candidatos y material pendiente del corpus elegible; verificar derechos de adquisición, entrenamiento y redistribución de forma independiente. Respetar privacidad, retiro y retención; un snapshot no prevalece sobre obligaciones de eliminación.

Generar un reporte a partir de los datos: documentos, tokens (tokenizer identificado), calidad, duplicados, cobertura, exclusiones y desconocidos. Distinguir textos humanos, verbalizaciones y sintéticos. Congelar mediante un manifiesto la versión del corpus y los splits usados en cada experimento; seguir ampliando el corpus local sin alterar ese experimento.

## Rigor, sin burocracia

- Integrar informática, ML, estadística/probabilidad, ciencias sociales, comunicación, lingüística y semiótica según la pregunta. Combinar mediciones con lectura cualitativa de textos, contexto y sesgos de selección.
- Definir la unidad de análisis y denominadores; usar muestreo, incertidumbre y controles cuando sean pertinentes. Disponibilidad digital no implica representatividad social; documentar límites y no extrapolar muestras de conveniencia.
- Distinguir exploración de confirmación. Fijar antes del experimento confirmatorio hipótesis, métricas, controles, corpus, semillas y criterios de análisis; separar el test reservado. Registrar desviaciones, no ajustar retrospectivamente al resultado.

## Qué queda versionado

Git conserva código, pruebas, planes, decisiones, dependencias y evidencia pequeña revisada; datos, pesos y resultados grandes o privados se conservan fuera de Git con manifiestos, hashes y acceso autorizado. Cada corrida registra ID, fecha, commit y estado del árbol, comando, versiones, entradas, hashes disponibles, salidas, errores y límites; en ML también hardware, semillas, métricas y coste. No subir secretos ni material sin permiso.

Usar las carpetas existentes: `docs/`, `tools/`, `tests/`, `evidence/`. Los datos locales viven en `workspace/` (configurable, ignorado por Git). Crear configuraciones y subcarpetas solo cuando hagan falta. Empezar con Python y archivos estructurados; evaluar Parquet, DVC u orquestación únicamente si una necesidad concreta lo justifica.

## Primer incremento

Ejecutar y revisar la [prueba de factibilidad](feasibility.md). Después, con alcance aprobado, incorporar un lote pequeño de una fuente autorizada, producir corpus real y reporte, repetir sin duplicados y comprobar reanudación, exclusión y reproducción desde un snapshot. No hace falta una CLI completa ni un corpus masivo para validar el circuito. El [plan MVP](mvp-plan.md) fija los gates del entrenamiento y la publicación.

