-- ============================================
-- PROYECTO CAPSTONE: NYC YELLOW TAXI ANALYSIS
-- Estructura de Base de Datos
-- ============================================

-- Paso 1: Crear la base de datos
-- CREATE DATABASE capstone_project; -- Ejecutar solo si no existe

-- Paso 2: Crear tabla de dimensión ZONAS
DROP TABLE IF EXISTS zonas CASCADE;

CREATE TABLE zonas (
    location_id     INTEGER PRIMARY KEY,
    borough         VARCHAR(100),
    zone            VARCHAR(100)
);

-- Paso 3: Crear tabla de hechos VIAJES
DROP TABLE IF EXISTS viajes CASCADE;

CREATE TABLE viajes (
    id                  SERIAL PRIMARY KEY,
    vendor_id           INTEGER,
    pickup_datetime     TIMESTAMP,
    dropoff_datetime    TIMESTAMP,
    passenger_count     INTEGER,
    trip_distance       NUMERIC(8,2),
    pickup_location_id  INTEGER,
    dropoff_location_id INTEGER,
    payment_type        INTEGER,
    fare_amount         NUMERIC(10,2),
    tip_amount          NUMERIC(10,2),
    total_amount        NUMERIC(10,2)
);

-- Paso 4: Crear tabla STAGING para viajes (aceptar todas las columnas del CSV)
DROP TABLE IF EXISTS staging_viajes CASCADE;

CREATE TABLE staging_viajes (
    unnamed             VARCHAR(50),
    vendor_id           INTEGER,
    tpep_pickup_datetime VARCHAR(100),
    tpep_dropoff_datetime VARCHAR(100),
    passenger_count     NUMERIC,
    trip_distance       NUMERIC,
    ratecode_id         NUMERIC,
    store_and_fwd_flag  VARCHAR(5),
    pu_location_id      INTEGER,
    do_location_id      INTEGER,
    payment_type        INTEGER,
    fare_amount         NUMERIC,
    extra               NUMERIC,
    mta_tax             NUMERIC,
    tip_amount          NUMERIC,
    tolls_amount        NUMERIC,
    improvement_surcharge NUMERIC,
    total_amount        NUMERIC
);

-- Paso 5: Cargar datos desde CSV
-- NOTA: Reemplazar rutas con las rutas reales de los archivos CSV
-- En Mac/Linux: usar /tmp/ o una ruta absoluta accesible a PostgreSQL

COPY zonas (location_id, borough, zone) 
FROM '/tmp/zonas_limpio.csv' 
DELIMITER ',' CSV HEADER;

COPY staging_viajes FROM '/tmp/2017_Yellow_Taxi_Trip_Data.csv' 
DELIMITER ',' CSV HEADER;

-- Paso 6: Limpiar e insertar en tabla VIAJES final
-- Aplicar COALESCE para nulos, validar fechas y ubicaciones
INSERT INTO viajes (
    vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
    trip_distance, pickup_location_id, dropoff_location_id,
    payment_type, fare_amount, tip_amount, total_amount
)
SELECT
    vendor_id,
    TO_TIMESTAMP(tpep_pickup_datetime, 'MM/DD/YYYY HH12:MI:SS AM'),
    TO_TIMESTAMP(tpep_dropoff_datetime, 'MM/DD/YYYY HH12:MI:SS AM'),
    COALESCE(passenger_count::INTEGER, 1),
    COALESCE(trip_distance, 0),
    pu_location_id,
    do_location_id,
    payment_type,
    COALESCE(fare_amount, 0),
    COALESCE(tip_amount, 0),
    COALESCE(total_amount, 0)
FROM staging_viajes
WHERE tpep_pickup_datetime IS NOT NULL
  AND pu_location_id IS NOT NULL
  AND do_location_id IS NOT NULL;

-- Paso 7: Verificación final
SELECT COUNT(*) AS total_viajes FROM viajes;
SELECT COUNT(*) AS total_zonas FROM zonas;
SELECT COUNT(*) AS nulos_fecha FROM viajes WHERE pickup_datetime IS NULL;
SELECT COUNT(*) AS nulos_ubicacion FROM viajes 
WHERE pickup_location_id IS NULL OR dropoff_location_id IS NULL;

-- Paso 8: Limpiar tabla staging (opcional)
-- DROP TABLE staging_viajes;
