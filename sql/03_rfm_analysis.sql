-- =========================================================================
-- 03 RFM PREPARATION & WINDOW FUNCTIONS
-- =========================================================================

-- 1. Total Unique Customer Count
SELECT
    COUNT(DISTINCT Customer) AS TotalCustomers
FROM factsales;

-- 2. Customer Concentration & Revenue Share (Window Functions)
SELECT
    Customer,
    SUM(`Value ( Quantity * Rate )`) AS Revenue,
    ROUND(
        SUM(`Value ( Quantity * Rate )`) * 100 / SUM(SUM(`Value ( Quantity * Rate )`)) OVER(),
        2
    ) AS RevenueSharePct
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC;

-- 3. Customer Rankings
SELECT
    Customer,
    SUM(`Value ( Quantity * Rate )`) AS Revenue,
    RANK() OVER(ORDER BY SUM(`Value ( Quantity * Rate )`) DESC) AS CustomerRank
FROM factsales
GROUP BY Customer;

-- 4. Product Revenue Rankings
SELECT
    Products,
    SUM(`Value ( Quantity * Rate )`) AS Revenue,
    RANK() OVER(ORDER BY SUM(`Value ( Quantity * Rate )`) DESC) AS ProductRank
FROM factsales
GROUP BY Products;

-- 5. Month-over-Month Growth Calculation (LAG)
WITH MonthlyRevenue AS (
    SELECT
        DATE_FORMAT(STR_TO_DATE(`Date`, '%d-%b-%y'), '%Y-%m') AS Month,
        SUM(`Value ( Quantity * Rate )`) AS Revenue
    FROM factsales
    GROUP BY Month
)
SELECT
    Month,
    Revenue,
    LAG(Revenue) OVER(ORDER BY Month) AS PrevRevenue,
    ROUND(
        (Revenue - LAG(Revenue) OVER(ORDER BY Month)) * 100 / LAG(Revenue) OVER(ORDER BY Month),
        2
    ) AS GrowthPct
FROM MonthlyRevenue;

-- 6. Cumulative Running Total Revenue
WITH MonthlyRevenue AS (
    SELECT
        DATE_FORMAT(STR_TO_DATE(`Date`, '%d-%b-%y'), '%Y-%m') AS Month,
        SUM(`Value ( Quantity * Rate )`) AS Revenue
    FROM factsales
    GROUP BY Month
)
SELECT
    Month,
    Revenue,
    SUM(Revenue) OVER(ORDER BY Month) AS RunningRevenue
FROM MonthlyRevenue;
