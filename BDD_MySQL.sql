USE mydatabase;

-- TABLA PARA ALMACENAMIENTO DE LOGS:
-- -----------------------------------------
DROP TABLE IF EXISTS nginx_logs;
CREATE TABLE nginx_logs (
    remote_port VARCHAR(10),
    remote_addr VARCHAR(20),
    remote_usr VARCHAR(50),
    loc_timestamp VARCHAR(50),
    request VARCHAR(200),
    status_req VARCHAR(50),
    body_bytes_sent VARCHAR(20),
    http_refer VARCHAR(100),
    http_usr_agent VARCHAR(100),
    http_x_forwarded_for VARCHAR(100),
    log_timestamp DATETIME
);


-- TABLA PARA ALMACENAMIENTO DE ERRORES:
-- -----------------------------------------
DROP TABLE IF EXISTS nginx_errors;
CREATE TABLE nginx_errors (
    message VARCHAR(200),
    error_timestamp DATETIME
);

-- TABLA PARA FLAG DE EJECUCION:
-- -----------------------------------------
DROP TABLE IF EXISTS airflow_bar_execution;
CREATE TABLE airflow_bar_execution (
    execution int
);

/*
INSERT INTO airflow_bar_execution
SELECT
1;
*/

-- TABLA LOG DE OVERLOADS:
-- -----------------------------------------
DROP TABLE IF EXISTS nginx_balance_overloads;
CREATE TABLE nginx_balance_overloads (
    old_port INT,
    percentage_reqs float,
    count_reqs float,
    over_timestamp DATETIME
);


-- SELECT TABLA LOGS
-- -----------------------------------------
SELECT
*
FROM nginx_logs;

-- SELECT TABLA ERRORES
-- -----------------------------------------
SELECT
*
FROM nginx_errors;

-- SELECT FLAG EJECUCION
-- -----------------------------------------
SELECT *
FROM airflow_bar_execution;

-- SELECT TABLA OVERLOADS
-- -----------------------------------------
SELECT
*
FROM nginx_balance_overloads;

-- CANCELAR DAGS MANUALMENTE
-- -----------------------------------------
/*
UPDATE airflow_bar_execution 
SET execution = 0;
*/

-- QUERY PARA CALCULO DE SERVICIO CON MAS TRAFICO
-- -----------------------------------------
SELECT 
    remote_port_int,
    percentage,
    total_reqs
FROM 
    (SELECT 
        COUNT(1) / (SELECT COUNT(1) FROM nginx_logs) AS percentage,
        COUNT(1) AS total_reqs,
        CAST(remote_port AS UNSIGNED) AS remote_port_int
    FROM nginx_logs
    GROUP BY CAST(remote_port AS UNSIGNED)) A
ORDER BY percentage DESC
LIMIT 1;
