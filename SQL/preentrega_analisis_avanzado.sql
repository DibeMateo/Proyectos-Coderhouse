-- =============================================
-- Pre-entrega Módulo 4: Análisis avanzado con Window Functions
-- Alumno: Di Benedetto Mateo
-- Fecha: 14/07/2026
-- =============================================

-- =============================================
-- CTE 1: ventas_mensuales
-- Agrupamos las ventas por mes y categoría para tener la base
-- de todas las métricas. Usamos DATE_TRUNC para normalizar
-- las fechas al primer día de cada mes.
-- =============================================

WITH ventas_mensuales AS (
    SELECT
        DATE_TRUNC('month', v.fecha) AS mes,
        cat.nombre AS categoria,
        SUM(v.cantidad * p.precio) AS venta_total
    FROM ventas v
    INNER JOIN productos p ON v.producto_id = p.id
    INNER JOIN categorias cat ON p.categoria_id = cat.id
    GROUP BY DATE_TRUNC('month', v.fecha), cat.nombre
),

-- =============================================
-- CTE 2: metricas_ventana
-- Sobre los datos agrupados, aplicamos window functions:
-- RANK() para rankear categorías dentro de cada mes.
-- SUM() OVER con ORDER BY para el acumulado progresivo.
-- AVG() OVER para el promedio histórico de cada categoría.
-- =============================================

metricas_ventana AS (
    SELECT
        mes,
        categoria,
        venta_total,
        RANK() OVER (PARTITION BY mes ORDER BY venta_total DESC) AS ranking_mes,
        SUM(venta_total) OVER (PARTITION BY categoria ORDER BY mes) AS acumulado,
        AVG(venta_total) OVER (PARTITION BY categoria) AS promedio_historico
    FROM ventas_mensuales
)

-- =============================================
-- CONSULTA FINAL
-- Usamos CASE WHEN para comparar la venta del mes contra
-- el promedio histórico de esa categoría. Si es mayor o igual
-- al promedio, es "Exitoso"; si no, queda "Bajo el promedio".
-- =============================================

SELECT
    TO_CHAR(mes, 'YYYY-MM') AS mes,
    categoria,
    venta_total,
    ranking_mes,
    acumulado,
    CASE
        WHEN venta_total >= promedio_historico THEN 'Exitoso'
        ELSE 'Bajo el promedio'
    END AS comparativa
FROM metricas_ventana
ORDER BY mes, ranking_mes;
