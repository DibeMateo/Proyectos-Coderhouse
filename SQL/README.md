# Análisis Exploratorio de Datos: NYC Yellow Taxi Trips 2017

## Problema de Negocio

En el mundo de los taxis en Nueva York, la pregunta clave no es simplemente "¿cuántos viajes hay?" sino "¿dónde están los viajes rentables y qué patrones definen el negocio?". Este proyecto simula el flujo de trabajo real de un analista de datos: limpiar datos del mundo real, construir un modelo relacional, y extraer insights accionables que el equipo directivo pueda usar para decisiones estratégicas.

Los taxis de NYC no son un servicio homogéneo: cada zona, cada hora del día, cada distancia tiene un perfil de ingresos y demanda diferente. Entender estas variaciones es crítico para:
- **Asignación de recursos**: ¿Dónde desplegar más taxis?
- **Precios dinámicos**: ¿Qué zonas pueden soportar tarifas más altas?
- **Planificación operativa**: ¿Hay épocas altas y bajas en el año?

## Hallazgos Principales

### 1. **Las zonas aeroportuarias dominan los ingresos** (Consulta 1)

| Zona | Borough | Viajes | Ingresos Totales | Distancia Promedio |
|------|---------|--------|------------------|--------------------|
| JFK Airport | Queens | 532 | $29,257.78 | 15.48 millas |
| LaGuardia Airport | Queens | 623 | $26,918.39 | 9.85 millas |
| Midtown Center | Manhattan | 861 | $12,753.76 | 2.32 millas |

**Interpretación**: Los aeropuertos generan aproximadamente **2.3× más ingresos que Midtown**, a pesar de que Midtown tiene más viajes. Esto se debe a las **distancias más largas** (15-16 millas vs 2 millas). Esta es la zona con mayor ROI por taxi asignado.

**Para el equipo directivo**: Priorizar colocación de taxis en aeropuertos. Cada taxi en JFK genera $55 de ingresos promedio vs $15 en Midtown Center.

---

### 2. **Estacionalidad detectada: verano es la temporada fuerte** (Consulta 2)

Analizando los 12 meses de 2017 (mostrados como 2017-01 a 2017-12):

- **Picos**: 03 (marzo, $33,065.83), 08 (agosto, $33,828.58) — primavera y verano
- **Valles**: 06 (junio, $26,617.64), 11 (noviembre, $27,759.56) — transiciones
- **Promedio por viaje**: Fluctúa entre $15.69 y $16.81 (variación de 7%), lo que indica que la demanda varía, no los precios

**Interpretación**: La estacionalidad es ligera pero consistente. Marzo y agosto son los meses con mayor demanda total de ingresos. Junio (aunque es verano) cae, sugiriendo que **julio y agosto roban demanda de junio** (vacaciones de verano). Noviembre cae, probablemente por la preparación para las fiestas de fin de año.

**Para el equipo directivo**: Planificar campañas de retención de conductores en marzo y agosto. En junio, ofertar incentivos para evitar que se vayan. Preparar volumen reducido en noviembre.

---

### 3. **Zonas fantasma: oportunidades sin explotar** (Consulta 3)

Estas tres zonas tienen **un solo viaje registrado en todo 2017**:

| Zona | Borough | Viajes | Ingresos |
|------|---------|--------|----------|
| Pelham Bay Park | Bronx | 1 | $10.80 |
| East Flushing | Queens | 1 | $33.80 |
| Van Cortlandt Park | Bronx | 1 | $33.92 |

**Interpretación**: Estas zonas están **completamente desatendidas**. No son zonas sin demanda (los parques son destinos turísticos), sino zonas sin **oferta visible** de taxis. Podrían ser oportunidades de nicho si se desplegaran taxis estratégicamente.

**Para el equipo directivo**: Estudiar por qué. ¿Son zonas remotas con transporte público bueno? ¿O solo falta marketing? Pequeña inversión piloto podría desbloquear mercado latente.

---

### 4. **La distribución de viajes es hiperconcentrada** (Consulta 4)

El **Top 10 por volumen** es casi todo Manhattan:

| Zona | Borough | Viajes | Ranking |
|------|---------|--------|---------|
| Upper East Side South | Manhattan | 890 | 1 |
| Midtown Center | Manhattan | 861 | 2 |
| Penn Station/Madison Sq | Manhattan | 792 | 3 |
| ... | Manhattan | ... | ... |
| Lincoln Square East | Manhattan | 649 | 10 |

9 de 10 son Manhattan. La próxima zona fuera de Manhattan no aparece hasta el ranking 11.

**Interpretación**: El negocio de taxis NYC es fundamentalmente un **negocio de Manhattan**. El volumen domina, pero no necesariamente la rentabilidad por viaje (porque las distancias son cortas: 2-3 millas). Este es el "pan de cada día" — volumen predecible pero márgenes bajos.

**Para el equipo directivo**: Mantener cobertura fuerte en Manhattan (volumen = estabilidad), pero no sobreinvertir ahí. Explorar "mercados de alto valor" como aeropuertos para margen por taxi.

---

### 5. **La relación distancia-ingresos es logarítmica, no lineal** (Consulta 5)

| Rango de Distancia | Viajes | Ingreso Promedio | Ingresos Totales |
|--------------------|--------|------------------|------------------|
| Muy corto (< 1 mi) | 5,539 | $7.64 | $42,302 |
| Corto (1-3 mi) | 11,270 | $12.37 | $139,460 |
| Medio (3-5 mi) | 2,560 | $20.09 | $51,434 |
| Largo (5-10 mi) | 1,884 | $31.16 | $58,708 |
| Muy largo (> 10 mi) | 1,298 | $57.21 | $74,253 |

**Interpretación**: 

- **Viajes muy cortos (< 1 milla)**: Bajo margen ($7.64), pero volumen masivo (5,539). Son "viajes de consuelo" — gente en Midtown que prefiere taxi a andar 6 cuadras.

- **Salto crítico en 1-3 millas**: El ingreso promedio casi se **duplica** ($7.64 → $12.37). Este es el "sweet spot" de demanda: cerca pero no muy cerca. Manhattan intra-barrio.

- **Viajes muy largos (> 10 millas)**: Ingreso promedio es **7.5× mayor** que muy cortos ($57.21 vs $7.64). Son raros (1,298 viajes vs 5,539), pero extremadamente rentables. Estos son mayormente aeropuertos.

**Curva de rentabilidad**:
```
Ingresos por viaje
       |
    $60 |           ●● (> 10 mi)
    $50 |         ●
    $40 |       ●
    $30 |     ●
    $20 |   ●
    $10 | ●●
       |_________________
         0   5   10  15  Distancia (millas)
```

La curva es **exponencial hacia distancias largas**. Cada milla extra de distancia agrega ingresos no linealmente.

**Para el equipo directivo**: Estrategia de dos capas:
1. **Volumen**: Mantener saturación en Manhattan (muy corto y corto = 16,809 viajes = 65% del volumen)
2. **Margen**: Capturar viajes largos activamente (aeropuertos, viajes inter-barrio)

---

## Técnicas SQL Utilizadas

### Limppieza de Datos
- **COALESCE()**: Rellenar nulos en columnas críticas (pasajeros → 1, distancia → 0, tarifas → 0)
- **WHERE IS NOT NULL**: Descartar filas con fechas o ubicaciones inválidas (crítico para JOIN)
- **Conversión de tipos**: `TO_TIMESTAMP()` para parsear fechas de múltiples formatos

### Análisis Exploratorio
- **GROUP BY + agregaciones**: Sumas, promedios, conteos por zona, mes, rango
- **INNER JOIN**: Conectar viajes con zonas; solo incluir ubicaciones válidas
- **ORDER BY / LIMIT**: Identificar tops y bottoms

### Técnicas Avanzadas
- **Window Functions (RANK, ROW_NUMBER)**: Ranking con `PARTITION BY` para top por borough
- **CASE statements**: Segmentación de viajes por distancia sin crear tablas nuevas
- **CTEs (WITH)**: Tabla temporal `rango_viajes` para organizar lógica compleja sin contaminar el query principal
- **TO_CHAR()**: Extracción de año-mes de timestamps para análisis temporal

---

## Instrucciones para Ejecutar

### 1. Preparar los datos

```bash
# En Mac, copiar CSVs a /tmp (PostgreSQL puede leer ahí)
cp /Users/dibemateo/Downloads/CODERHOUSE/SQL/2017_Yellow_Taxi_Trip_Data.csv /tmp/
cp /Users/dibemateo/Downloads/CODERHOUSE/SQL/NYC_Taxi_Zones_20260729.csv /tmp/
```

(Nota: El archivo de zonas requiere limpieza previa en Excel para quedarse solo con las columnas `location_id`, `borough`, `zone`)

### 2. Crear la base de datos y estructura

```bash
psql -U postgres
CREATE DATABASE capstone_project;
\c capstone_project
\i estructura.sql
```

### 3. Ejecutar el análisis

```bash
\i analisis.sql
```

Esto ejecutará las 5 consultas secuencialmente.

---

## Conclusiones para el Equipo Ejecutivo

| Pregunta | Hallazgo | Acción |
|----------|----------|--------|
| ¿Dónde invierto en taxis? | Aeropuertos generan 2.3× más que Midtown | Aumentar flotas en JFK/LaGuardia |
| ¿Cuándo aumenta la demanda? | Marzo y agosto; junio cae | Planificar incentivos en marzo/agosto |
| ¿Hay mercados nuevos? | Parques (Bronx, Queens) tienen 1 viaje/año | Piloto de 5-10 taxis en East Flushing |
| ¿Qué viajes son rentables? | Largo plazo (5-10 mi, >10 mi) = $31-$57/viaje | Priorizar captación de viajes de distancia |
| ¿Qué volumen tengo? | 65% en Manhattan; muy concentrado | Riesgo regulatorio; diversificar |

---

## Archivos Entregables

- **`estructura.sql`**: Creación de tablas, limpieza, carga de datos
- **`analisis.sql`**: Las 5 consultas con comentarios explicativos
- **`README.md`**: Este documento

**Autor**: Mateo Di Benedetto  
**Curso**: Coderhouse — SQL (Capstone Project)  
**Dataset**: NYC Yellow Taxi Trip Data 2017  
**Fecha**: 2026
