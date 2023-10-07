-- CREATE RDBMS FOR CHEM TEMP

-- Set schema name
SET SCHEMA 'chemtemp';

DROP TABLE IF EXISTS "sensor_data"
;

DROP SEQUENCE IF EXISTS "sensor_data_id seq"
;

CREATE SEQUENCE "sensor_data_id_seq"
  AS integer
  INCREMENT BY 1
  START WITH 1
  NO MINVALUE
  CACHE 1
;


CREATE TABLE "sensor_data"
(
  "id" Integer DEFAULT nextval('sensor_data_id_seq'::regclass) NOT NULL,
  "device_address" Character varying(20) NOT NULL,
  "sensor_type" Character varying(1) NOT NULL,
  "sensor_value" Character varying(20) NOT NULL,
  "created_at" Timestamp with time zone DEFAULT now() NOT NULL
)
WITH (
  autovacuum_enabled=true)
;

ALTER TABLE "sensor_data" ADD CONSTRAINT "PK_sensor_data" PRIMARY KEY ("id")
;

