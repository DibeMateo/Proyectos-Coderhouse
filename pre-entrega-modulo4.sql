-- =============================================
-- Pre-entrega Módulo 4: Consultas multicapa para análisis de negocio
-- Alumno: Di Benedetto Mateo
-- Fecha: 14/07/2026
-- =============================================

-- =============================================
-- CONSULTA 1: Rentabilidad por categoría
-- Problema de negocio: Se necesita saber qué categorías de productos
-- son las que más plata generan, para ver dónde conviene invertir
-- más en stock o en publicidad. Unimos ventas, productos y categorías
-- para ver unidades vendidas y el ingreso total por cada categoría.
-- Filtramos con HAVING para quedarnos solo con las categorías que
-- superen un umbral de ingreso (en este caso 10000).
-- =============================================

SELECT
    cat.nombre AS categoria,
    SUM(v.cantidad) AS unidades_vendidas,
    SUM(v.cantidad * p.precio) AS ingreso_total
FROM ventas v
INNER JOIN productos p ON v.producto_id = p.id
INNER JOIN categorias cat ON p.categoria_id = cat.id
GROUP BY cat.nombre
HAVING SUM(v.cantidad * p.precio) > 10000
ORDER BY ingreso_total DESC;

-- =============================================
-- CONSULTA 2: Clientes escurridizos (sin compras)
-- Problema de negocio: Hay clientes que se registraron pero nunca
-- compraron nada. Con un LEFT JOIN podemos detectar cuáles son,
-- para mandarles una promoción o verificar si son datos inválidos.
-- Usamos COALESCE para que en lugar de NULL aparezque 0 en
-- la cantidad de compras, así queda más claro en el reporte.
-- =============================================

SELECT
    c.id AS cliente_id,
    c.nombre,
    c.email,
    COALESCE(COUNT(v.id), 0) AS cantidad_compras
FROM clientes c
LEFT JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.id, c.nombre, c.email
HAVING COUNT(v.id) = 0
ORDER BY c.nombre;

-- =============================================
-- CONSULTA 3: Top de compras por cliente
-- Problema de negocio: Queremos saber cuáles son nuestros mejores
-- clientes, qué producto compraron más veces y cuándo fue su última
-- compra. Esto sirve para armar programas de fidelización o
-- detectar tendencias de compra por cliente.
-- Unimos clientes, ventas y productos. Usamos una subconsulta
-- para calcular el producto más comprado por cada cliente.
-- =============================================

SELECT
    c.nombre AS cliente,
    p.nombre AS producto_mas_comprado,
    MAX(v.fecha) AS ultima_transaccion,
    COUNT(v.id) AS total_compras
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
INNER JOIN productos p ON v.producto_id = p.id
GROUP BY c.nombre, p.nombre
ORDER BY total_compras DESC
LIMIT 10;
