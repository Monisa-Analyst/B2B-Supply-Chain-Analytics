-- =========================================================================
-- 02 KPI & TREND QUERIES
-- =========================================================================

-- 1. Total Net Revenue
SELECT
    SUM(`Value ( Quantity * Rate )`) AS TotalRevenue
FROM factsales;

-- 2. Monthly Revenue Trend
SELECT
    DATE_FORMAT(STR_TO_DATE(`Date`, '%d-%b-%y'), '%Y-%m') AS Month,
    SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
ORDER BY Month;

-- 3. Monthly Revenue Target Thresholds
SELECT
    DATE_FORMAT(STR_TO_DATE(`Date`, '%d-%b-%y'), '%Y-%m') AS Month,
    SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
HAVING Revenue < 2000000
ORDER BY Month;

-- 4. Customer Revenue Leaderboard
SELECT
    Customer,
    SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC;

-- 5. Top 10 Product Leaderboard (Revenue)
SELECT
    Products,
    SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Products
ORDER BY Revenue DESC
LIMIT 10;

-- 6. Top 10 Product Leaderboard (Units Sold)
SELECT
    Products,
    SUM(Quantity) AS UnitsSold
FROM factsales
GROUP BY Products
ORDER BY UnitsSold DESC
LIMIT 10;
