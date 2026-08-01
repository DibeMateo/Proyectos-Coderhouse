-- ============================================
-- ANÁLISIS DE VIAJES NYC TAXIS 2017
-- Consultas comentadas que responden preguntas de negocio
-- ============================================

-- CONSULTA 1: Top 5 zonas de origen por ingresos totales
-- Pregunta: ¿De dónde salen los viajes más rentables?
-- Por qué: Identificar qué zonas generan más valor para optimizar disponibilidad de taxis
SELECT 
    z.zone AS zona_origen,
    z.borough,
    COUNT(*) AS cantidad_viajes,
    ROUND(SUM(v.fare_amount)::NUMERIC, 2) AS ingresos_tarifa,
    ROUND(SUM(v.tip_amount)::NUMERIC, 2) AS propinas_totales,
    ROUND(SUM(v.total_amount)::NUMERIC, 2) AS ingresos_totales,
    ROUND(AVG(v.trip_distance)::NUMERIC, 2) AS distancia_promedio
FROM viajes v
INNER JOIN zonas z ON v.pickup_location_id = z.location_id
GROUP BY z.location_id, z.zone, z.borough
ORDER BY ingresos_totales DESC
LIMIT 5;

-- CONSULTA 2: Ingresos totales por mes (usando funciones de fecha)
-- Pregunta: ¿En qué meses hay más ingresos? ¿Hay estacionalidad?
-- Por qué: Detectar patrones mensuales para planificación de recursos y marketing
SELECT 
    TO_CHAR(v.pickup_datetime, 'YYYY-MM') AS mes,
    COUNT(*) AS viajes_en_mes,
    ROUND(SUM(v.fare_amount)::NUMERIC, 2) AS tarifa_mes,
    ROUND(SUM(v.tip_amount)::NUMERIC, 2) AS propinas_mes,
    ROUND(SUM(v.total_amount)::NUMERIC, 2) AS ingresos_mes,
    ROUND(AVG(v.total_amount)::NUMERIC, 2) AS promedio_por_viaje
FROM viajes v
WHERE v.pickup_datetime IS NOT NULL
GROUP BY TO_CHAR(v.pickup_datetime, 'YYYY-MM')
ORDER BY mes DESC;

-- CONSULTA 3: Top 3 zonas de DESTINO menos utilizadas
-- Pregunta: ¿Hay zonas que pocos pasajeros visitan?
-- Por qué: Identificar oportunidades de mercado o problemas de accesibilidad
SELECT 
    z.zone AS zona_destino,
    z.borough,
    COUNT(*) AS cantidad_viajes_destino,
    ROUND(AVG(v.trip_distance)::NUMERIC, 2) AS distancia_promedio,
    ROUND(SUM(v.total_amount)::NUMERIC, 2) AS ingresos_a_zona
FROM viajes v
INNER JOIN zonas z ON v.dropoff_location_id = z.location_id
GROUP BY z.location_id, z.zone, z.borough
ORDER BY cantidad_viajes_destino ASC
LIMIT 3;

-- CONSULTA 4: Ranking de zonas de ORIGEN por cantidad de viajes (Window Function)
-- Pregunta: ¿Cuál es la posición de cada zona por volumen de viajes?
-- Por qué: Uso de RANK() (Window Function) para ranking con empates, 
--          y ROW_NUMBER() para ranking dentro de cada borough (PARTITION BY)
SELECT 
    z.zone AS zona_origen,
    z.borough,
    COUNT(*) AS cantidad_viajes,
    ROUND(SUM(v.total_amount)::NUMERIC, 2) AS ingresos,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS ranking_por_viajes,
    ROW_NUMBER() OVER (PARTITION BY z.borough ORDER BY COUNT(*) DESC) AS ranking_en_borough
FROM viajes v
INNER JOIN zonas z ON v.pickup_location_id = z.location_id
GROUP BY z.location_id, z.zone, z.borough
ORDER BY ranking_por_viajes ASC
LIMIT 10;

-- CONSULTA 5: Análisis de distancia vs ingresos (CASE statement + CTE)
-- Pregunta: ¿Los viajes largos generan más ingresos que los cortos?
-- Por qué: Segmentar viajes por distancia (CASE) para ver patrones de rentabilidad.
--          Usar CTE (WITH) para crear columnas auxiliares sin contaminar el análisis final.
WITH rango_viajes AS (
  SELECT 
    v.*,
    CASE 
      WHEN v.trip_distance < 1 THEN 'Muy corto (< 1 milla)'
      WHEN v.trip_distance BETWEEN 1 AND 3 THEN 'Corto (1-3 millas)'
      WHEN v.trip_distance BETWEEN 3 AND 5 THEN 'Medio (3-5 millas)'
      WHEN v.trip_distance BETWEEN 5 AND 10 THEN 'Largo (5-10 millas)'
      ELSE 'Muy largo (> 10 millas)'
    END AS rango_distancia,
    CASE 
      WHEN v.trip_distance < 1 THEN 1
      WHEN v.trip_distance BETWEEN 1 AND 3 THEN 2
      WHEN v.trip_distance BETWEEN 3 AND 5 THEN 3
      WHEN v.trip_distance BETWEEN 5 AND 10 THEN 4
      ELSE 5
    END AS orden
  FROM viajes v
  WHERE v.trip_distance IS NOT NULL AND v.trip_distance > 0
)
SELECT 
  rango_distancia,
  COUNT(*) AS cantidad_viajes,
  ROUND(AVG(trip_distance)::NUMERIC, 2) AS distancia_promedio,
  ROUND(AVG(fare_amount)::NUMERIC, 2) AS tarifa_promedio,
  ROUND(AVG(tip_amount)::NUMERIC, 2) AS propina_promedio,
  ROUND(AVG(total_amount)::NUMERIC, 2) AS ingreso_promedio,
  ROUND(SUM(total_amount)::NUMERIC, 2) AS ingresos_totales
FROM rango_viajes
GROUP BY rango_distancia, orden
ORDER BY orden;
