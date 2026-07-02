-- =====================================================================
-- Pre-entrega: Consultas multicapa para análisis de negocio
-- Base de datos: retail_project
-- Objetivo: extraer inteligencia de negocio combinando múltiples tablas
--           mediante JOINs, GROUP BY y HAVING.
-- =====================================================================

-- =====================================================================
-- 0. EXTENSIÓN DE ESQUEMA (ejecutar solo si tu base todavía no tiene
--    la tabla "categorias" del módulo anterior). Si ya la tenés cargada
--    con datos, saltá directo a la sección 1.
-- =====================================================================

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria    SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(50) NOT NULL UNIQUE
);

-- Agrega la relación productos -> categorias (si tu tabla "productos"
-- todavía guarda la categoría como texto libre, migrala a esta FK).
ALTER TABLE productos
    ADD COLUMN IF NOT EXISTS id_categoria INT REFERENCES categorias (id_categoria);

-- Carga de categorías base
INSERT INTO categorias (nombre_categoria) VALUES
    ('Tecnología'), ('Indumentaria'), ('Hogar')
ON CONFLICT (nombre_categoria) DO NOTHING;

-- Asocia los productos existentes a su categoría correspondiente
UPDATE productos SET id_categoria = (SELECT id_categoria FROM categorias WHERE nombre_categoria = productos.categoria)
WHERE id_categoria IS NULL;

-- =====================================================================
-- 1. RENTABILIDAD POR CATEGORÍA
-- ---------------------------------------------------------------------
-- Problema de negocio: identificar qué categorías de productos generan
-- mayor volumen de unidades vendidas e ingreso total, para priorizar
-- inversión en stock y marketing. Se filtran solo las categorías que
-- superan un umbral de ingreso de $100.000 (definido según el negocio).
-- =====================================================================
SELECT
    cat.nombre_categoria                       AS categoria,
    SUM(v.cantidad)                            AS unidades_vendidas,
    SUM(v.cantidad * p.precio)                 AS ingreso_total
FROM ventas v
JOIN productos p   ON v.id_producto = p.id_producto
JOIN categorias cat ON p.id_categoria = cat.id_categoria
GROUP BY cat.nombre_categoria
HAVING SUM(v.cantidad * p.precio) > 100000          -- filtro sobre resultado agregado: va en HAVING, no en WHERE
ORDER BY ingreso_total DESC;

-- =====================================================================
-- 2. CLIENTES SIN COMPRAS ("clientes escurridizos")
-- ---------------------------------------------------------------------
-- Problema de negocio: detectar clientes registrados que nunca
-- concretaron una compra, para dirigir campañas de reactivación.
-- Se usa LEFT JOIN para conservar todos los clientes aunque no tengan
-- ventas asociadas, y COALESCE para mostrar 0 en lugar de NULL en el
-- conteo de compras.
-- =====================================================================
SELECT
    c.id_cliente,
    c.nombre,
    c.email,
    COALESCE(COUNT(v.id_venta), 0)             AS total_compras
FROM clientes c
LEFT JOIN ventas v ON c.id_cliente = v.id_cliente
GROUP BY c.id_cliente, c.nombre, c.email
HAVING COUNT(v.id_venta) = 0                   -- clientes con cero compras
ORDER BY c.nombre;

-- =====================================================================
-- 3. TOP DE COMPRAS POR CLIENTE
-- ---------------------------------------------------------------------
-- Problema de negocio: saber, para cada cliente, cuál es el producto
-- que más veces compró y cuándo fue la última vez que lo compró.
-- Esto ayuda a personalizar recomendaciones y detectar productos
-- "ancla" de cada cliente. Se arma una tabla intermedia (CTE) con el
-- conteo de compras por cliente-producto y se elige, con ROW_NUMBER(),
-- el producto más comprado de cada cliente (desempatando por la fecha
-- de compra más reciente).
-- =====================================================================
WITH conteo_producto_cliente AS (
    SELECT
        c.id_cliente,
        c.nombre                               AS nombre_cliente,
        p.nombre                                AS producto,
        COUNT(*)                                AS veces_comprado,
        MAX(v.fecha_venta)                      AS ultima_compra_producto,
        ROW_NUMBER() OVER (
            PARTITION BY c.id_cliente
            ORDER BY COUNT(*) DESC, MAX(v.fecha_venta) DESC
        )                                        AS ranking
    FROM clientes c
    JOIN ventas v    ON c.id_cliente = v.id_cliente
    JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY c.id_cliente, c.nombre, p.nombre
)
SELECT
    nombre_cliente,
    producto                                    AS producto_mas_comprado,
    veces_comprado,
    ultima_compra_producto                      AS fecha_ultima_transaccion
FROM conteo_producto_cliente
WHERE ranking = 1
ORDER BY nombre_cliente;
