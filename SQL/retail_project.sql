-- =====================================================================
-- Proyecto: retail_project
-- Descripción: Esquema base con tablas clientes, productos y ventas,
--              restricciones de integridad y carga inicial de datos.
-- Motor: PostgreSQL
-- =====================================================================

-- =====================================================================
-- 0. CREACIÓN DE LA BASE DE DATOS
-- =====================================================================
-- Ejecutar esta sentencia conectado a una base existente (ej: postgres).
-- Luego conectarse a retail_project antes de correr el resto del script.
CREATE DATABASE retail_project;

-- \c retail_project   -- (descomentar si se ejecuta desde psql)

-- =====================================================================
-- 1. DDL - ESTRUCTURA DE TABLAS
-- =====================================================================

-- ---------------------------------------------------------------------
-- Tabla: clientes
-- Se crea primero porque "ventas" depende de ella mediante FOREIGN KEY.
-- ---------------------------------------------------------------------
CREATE TABLE clientes (
    id_cliente   SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    edad         INT NOT NULL CHECK (edad >= 18),
    fecha_alta   DATE NOT NULL DEFAULT CURRENT_DATE
);

-- ---------------------------------------------------------------------
-- Tabla: productos
-- Se crea segundo, también requerida por "ventas" antes de existir esta.
-- ---------------------------------------------------------------------
CREATE TABLE productos (
    id_producto  SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    categoria    VARCHAR(50) NOT NULL,
    precio       DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock        INT NOT NULL CHECK (stock >= 0)
);

-- ---------------------------------------------------------------------
-- Tabla: ventas
-- Se crea última: contiene las FOREIGN KEY hacia clientes y productos.
-- ---------------------------------------------------------------------
CREATE TABLE ventas (
    id_venta      SERIAL PRIMARY KEY,
    id_cliente    INT NOT NULL,
    id_producto   INT NOT NULL,
    cantidad      INT NOT NULL CHECK (cantidad > 0),
    fecha_venta   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ventas_clientes
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_ventas_productos
        FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
);

-- =====================================================================
-- 2. DML - CARGA INICIAL DE DATOS (transacción explícita)
-- =====================================================================
BEGIN;

-- ----- clientes (5 registros) -----
INSERT INTO clientes (nombre, email, edad, fecha_alta) VALUES
    ('Mateo Di Benedetto', 'mateo.dibenedetto@example.com', 25, '2026-01-15'),
    ('Lucía Fernández',    'lucia.fernandez@example.com',   32, '2026-02-03'),
    ('Juan Pérez',         'juan.perez@example.com',        41, '2026-02-20'),
    ('Ana Gómez',          'ana.gomez@example.com',         29, '2026-03-05'),
    ('Carlos Ruiz',        'carlos.ruiz@example.com',       19, '2026-03-18');

-- ----- productos (5 registros) -----
INSERT INTO productos (nombre, categoria, precio, stock) VALUES
    ('Notebook 15"',        'Tecnología', 850000.00, 12),
    ('Mouse inalámbrico',   'Tecnología',  15000.00, 80),
    ('Zapatillas running',  'Indumentaria', 65000.00, 40),
    ('Campera impermeable', 'Indumentaria', 90000.00, 25),
    ('Cafetera eléctrica',  'Hogar',        45000.00, 15);

-- ----- ventas (5 registros) -----
INSERT INTO ventas (id_cliente, id_producto, cantidad, fecha_venta) VALUES
    (1, 1, 1, '2026-04-01 10:15:00'),
    (2, 2, 2, '2026-04-02 11:30:00'),
    (3, 3, 1, '2026-04-03 09:45:00'),
    (4, 4, 1, '2026-04-04 16:20:00'),
    (5, 5, 3, '2026-04-05 14:05:00');

COMMIT;

-- =====================================================================
-- 3. DML - MANTENIMIENTO
-- =====================================================================

-- ---------------------------------------------------------------------
-- UPDATE masivo: aumenta 10% el precio de todos los productos
-- de la categoría 'Tecnología'.
-- ---------------------------------------------------------------------

-- Verificación previa (recomendado antes de correr el UPDATE real):
-- SELECT * FROM productos WHERE categoria = 'Tecnología';

UPDATE productos
SET precio = ROUND(precio * 1.10, 2)
WHERE categoria = 'Tecnología';

-- ---------------------------------------------------------------------
-- DELETE puntual: elimina una venta de prueba específica.
-- ---------------------------------------------------------------------

-- Verificación previa (recomendado antes de correr el DELETE real):
-- SELECT * FROM ventas WHERE id_venta = 5;

DELETE FROM ventas
WHERE id_venta = 5;
