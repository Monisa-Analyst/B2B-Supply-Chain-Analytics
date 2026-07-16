-- =========================================================================
-- 01 DATA CLEANING & SCHEMA DDL
-- =========================================================================

-- 1. Table schema DDL definition
CREATE TABLE factsales (
    Date VARCHAR(20),
    Customer VARCHAR(255),
    Products VARCHAR(255),
    Quantity DOUBLE,
    Rate DOUBLE,
    `Value ( Quantity * Rate )` DOUBLE
);

-- 2. Verify total row count loaded
SELECT COUNT(*) AS TotalRows
FROM factsales;

-- 3. Sample check of raw transaction lines
SELECT *
FROM factsales
LIMIT 10;

-- 4. Audit check: Verify if calculated field matches quantity * rate
SELECT 
    COUNT(*) AS DiscrepancyCount
FROM factsales
WHERE ROUND(`Value ( Quantity * Rate )`, 2) != ROUND(Quantity * Rate, 2);
