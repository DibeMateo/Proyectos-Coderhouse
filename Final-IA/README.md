# Agente de Búsqueda Laboral Diaria

Ecosistema de automatización con IA desarrollado como Entrega Final del curso de automatización. Tiene dos flujos: uno busca ofertas de Analista de Datos todos los días y las evalúa con un modelo de lenguaje; el otro pide aprobación humana antes de postular.

Autor: Mateo Di Benedetto

---

## 1. Caso de uso

Revisión diaria de ofertas laborales para Analista de Datos (modalidad remota, que es la fuente disponible). Cada oferta nueva se compara contra las ya registradas, se puntúa según el perfil del candidato con Gemini y, si cumple el umbral de 50 sobre 100, se guarda en Notion y se incluye en el resumen del día.

Ninguna postulación sale sin aprobación humana: el Flujo 2 no envía nada hasta que la oferta tenga el checkbox **Aprobado** tildado.

## 2. Tecnologías

| Rol en el sistema | Tecnología |
|---|---|
| Orquestador | n8n (cuenta gratuita) |
| Base de datos y memoria | Notion: dos tablas relacionadas (Work Application Tracker y Empresas) |
| Motor de razonamiento (LLM) | Google Gemini (modelo Flash, API gratuita), solo en el Flujo 1 |
| Fuente de datos | API pública de Remotive (sin clave) |
| Canal de salida | Gmail |

## 3. Base de datos (Notion)

**Work Application Tracker** (una fila por oferta)

| Columna | Tipo | Uso |
|---|---|---|
| Task name | Title | Título de la oferta |
| Job URL | URL | Enlace a la oferta; sirve para no repetir ofertas |
| Empresa | Relation → Empresas | Vincula la oferta con su empresa |
| Score | Number | Puntaje de 0 a 100 dado por Gemini |
| Fecha detectada | Date | Día en que se encontró la oferta |
| Status | Status | Nuevo match, Quiero postular, Esperando aprobación, Postulación enviada, Rechazado |
| Carta generada | Text | Carta de presentación armada por el Flujo 2 |
| Aprobado | Checkbox | Aprobación humana: sin esta marca, no se envía nada |
| Error | Text | Mensaje de error cuando falla un envío o la IA |

**Empresas** (una fila por empresa)

| Columna | Tipo | Uso |
|---|---|---|
| Nombre | Title | Nombre de la empresa |
| Work Application Tracker | Relation (inversa) | Lista las ofertas de esa empresa |

La relación evita datos aislados: cada oferta apunta a una sola empresa, y una empresa puede tener varias ofertas.

**Enlaces a las bases de datos (modo lectura)**

- Work Application Tracker: https://cooked-growth-5d1.notion.site/3f15661db3e580b9beb7ce9a8a47e4a5?v=3f15661db3e5809aa2b9000cb726820b
- Empresas: https://cooked-growth-5d1.notion.site/3f85661db3e58023b50bde5124681958?v=3f85661db3e580fea0a5000c338dade5


## 4. Flujo 1: búsqueda, puntaje y resumen diario

Workflow: *Agente_Busqueda_Laboral_Diaria*. Trigger diario a las 12:00.

1. **Trigger: Revisión diaria mediodia** (Schedule, 12:00).
2. **Buscar ofertas (Remotive API)**: HTTP Request a la API de Remotive.
3. **Separar ofertar individuales** (Split Out sobre el campo `jobs`).
4. **Notion: leer ofertas ya procesadas** (Get many, Always Output Data), que alimenta a:
5. **Compare Datasets**: deja pasar solo las ofertas cuyo `url` no está en Job URL.
6. **Limitar ofertas por corrida** (Limit 1 por corrida): controla la cuota gratuita de Gemini.
7. **Esperar entre ofertas** (Wait 15 s).
8. **Nodo IA: Score de Fit (Gemini)**: devuelve un JSON con `score` y `motivo`. Retry On Fail (2 intentos), Max Output Tokens limitado a 300.
9. **Code: Interpretar respuesta IA**: lee el JSON; si la respuesta no es válida, el score queda en 0 y el motivo registra el error.
10. **Decisión: ¿cumple 50%?** (IF Number ≥ 50).
11. **Notion: Registrar oferta**: crea la fila (título, URL, score, fecha, Status). La columna Empresas (relación con la tabla Empresas) existe en el esquema, pero el flujo entregado no la completa automáticamente.
12. **Agrupar ofertas del día** (Aggregate) → **Armar mail del día** (Code, arma el HTML) → **Hay ofertas hoy** (IF count > 0) → **Gmail: Enviar resumen diario**.

Solo las ofertas que cumplen el umbral (score ≥ 50) se guardan en Notion. Si la IA falla (por ejemplo, cuota agotada), el Code deja score 0 con el error en `motivo` y la oferta no se registra, de modo que se reevalúa en la próxima corrida.

## 5. Flujo 2: aprobación humana y envío

Workflow: *Agente_Postulacion_HITL*. Dos ramas independientes que se comunican solo a través de Notion. **Este flujo no usa Gemini**: la carta es una plantilla fija, para no gastar la cuota de la IA.

**Rama 1: preparar la carta y pedir aprobación**
1. Schedule Trigger (cada hora).
2. Notion: buscar "Quiero postular" (Get many con filtro Status).
3. Hay oferta? (IF con id no vacío).
4. Code: armar carta (plantilla con título y Job URL).
5. Notion: esperando aprobación (Status = Esperando aprobación y Carta generada).
6. Gmail: pedir aprobación (mail de revisión). Si falla, salida Error → Notion: registrar error del mail (Status Rechazado).

**Rama 2: enviar la postulación tras la aprobación**
1. Schedule Trigger (cada hora, a los 30 minutos).
2. Notion: buscar aprobadas (Status = Esperando aprobación **y** Aprobado = true).
3. Hay aprobadas? (IF con id no vacío).
4. Code: preparar postulación (lee la carta guardada).
5. Gmail: enviar postulación (simulada). El destinatario es el propio correo del candidato, por la limitación descrita abajo. Si falla, salida Error → Notion: registrar error del mail.
6. Notion: marcar postulación enviada (Status = Postulación enviada).

## 6. Manejo de errores

- **Reintentos:** el nodo de Gemini reintenta hasta 5 veces con espera de 2 segundos.
- **Respuesta inválida:** si el modelo no devuelve un JSON legible, el score queda en 0 y el motivo registra el error. El flujo no se detiene.
- **Sin resultados:** los nodos de Notion tienen Always Output Data, así el flujo sigue aunque no haya filas.
- **Falla de envío de mail:** los nodos Gmail tienen la salida de error activada. Esa salida va a un nodo de Notion que cambia el Status a Rechazado y guarda el mensaje en la columna Error.
- **Sin ofertas que enviar:** los IF evitan mandar mails vacíos.

## 7. Gobernanza y consideraciones de datos

- Solo se envían a la IA la descripción pública del puesto y el perfil profesional del candidato.
- La IA califica y resume. No toma decisiones con efecto legal; la decisión de postularse es siempre humana.
- Las credenciales (API keys de Gemini, Notion y Gmail) se guardan en n8n y no están en este repositorio. Los JSON exportados no contienen claves.

## 8. Decisiones de diseño

- **Gemini en lugar de Claude u OpenAI:** se eligió Gemini porque su plan gratuito permite usar la API sin cargar un medio de pago, lo que era una restricción del proyecto. Se acota su uso a un solo nodo (el Flujo 1) y a 5 ofertas por corrida.
- **Dos tablas relacionadas:** Empresas y Work Application Tracker, para evitar datos aislados.
- **Carta por plantilla en el Flujo 2:** la IA no es necesaria para la aprobación humana, y así el segundo flujo no depende de la cuota.

## 9. Limitaciones conocidas

1. **Cuota gratuita de Gemini.** El modelo permite pocos pedidos por minuto y por día. Por eso el flujo limita a 5 ofertas por corrida y espacia los pedidos. Si se agota la cuota, el resumen de ese día puede salir incompleto.
2. **Fuente remota.** Remotive publica casi solo ofertas de trabajo remoto. No hay ofertas presenciales en Bahía Blanca, que es la localidad del candidato. El flujo busca ofertas remotas, que es la modalidad que el candidato también acepta.
3. **Saturación del servicio.** Gemini puede devolver errores 503 en horarios de alta demanda. El flujo reintenta, pero si el servicio sigue caído, esa corrida no genera resultados.
4. **Postulación simulada.** Las ofertas públicas no siempre traen un correo de contacto de la empresa. Por eso la postulación se dirige al propio correo del candidato. La aprobación humana sí está implementada como condición previa.
5. **Carta por plantilla.** La carta del Flujo 2 no está personalizada por la IA. Es una decisión para no consumir la cuota gratuita.

## 10. Cómo reproducirlo

1. Crear en Notion las dos tablas con las columnas de la sección 3, y compartirlas con la integración de Notion.
2. Importar `Agente_Busqueda_Laboral_Diaria.json` e `Agente_Postulacion_HITL.json` en n8n (menú "..." → Import from file).
3. Configurar las credenciales: Notion (OAuth), Google Gemini (API key de AI Studio) y Gmail (OAuth2).
4. Reemplazar el correo de destino (`REEMPLAZAR_TU_CORREO`) por el propio en los nodos Gmail.
5. Ejecutar cada flujo con "Test workflow" antes de activarlo.

## 11. Archivos del repositorio

- `README.md`: este documento.
- `Agente_Busqueda_Laboral_Diaria.json`: exportación del Flujo 1 (el correo de destino está reemplazado por un placeholder).
- `Agente_Postulacion_HITL.json`: exportación del Flujo 2 (idem).
- `Diagrama_Arquitectura_Agente_Busqueda_Laboral.pdf`: diagrama de arquitectura.
- `capturas/`: evidencias del flujo creado y de su ejecución (lienzo de los flujos y caso de error por cuota de Gemini).
- `videos/`: grabaciones de pantalla de las pruebas del 19 y 20 de octubre de 2026 (la del 20/10 a las 09:16, `prueba_flujo1_20-10_09-16_camino_feliz.mp4`, termina con el resumen diario llegando a Gmail), sin audio, con las credenciales fuera de cuadro.

## 12. Estado del proyecto (al momento de la entrega)

- **Flujo 1:** probado de punta a punta el 20/10: Gemini evaluó la oferta, Notion la registró y llegó el resumen por Gmail. La oferta evaluada (score 25) figura como *Descartada*, y el mail lista todas las ofertas evaluadas marcando cuáles son aptas (score ≥ 50). El 19/10 se registró además el camino infeliz: la cuota gratuita de Gemini se agotó y las ofertas quedaron con score 0 y el error en `motivo` (ver `capturas/03_...`). **Pendiente:** observar una oferta con score ≥ 50 como *Apta* en el mail.
- **Flujo 2:** armado y ejecutado en n8n (ver `videos/`). Sin Gemini, para no consumir cuota.
- **Pendientes:** Error Workflow central, prueba de estrés de 5 corridas con camino infeliz, y video demo de 3 minutos.
- Los JSON de este repositorio son los últimos exportados; antes de reproducirlos, revisar los nodos de Notion (selección de tabla y propiedades) y los de Gmail (correo de destino).
