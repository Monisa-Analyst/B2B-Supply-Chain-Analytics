SELECT
COUNT(DISTINCT Customer) AS TotalCustomers
FROM factsales;

SELECT
Customer,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC;

SELECT
Customer,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC
LIMIT 10;

SELECT
Customer,
SUM(`Value ( Quantity * Rate )`) AS Revenue,
ROUND(
SUM(`Value ( Quantity * Rate `)) * 100 /
SUM(SUM(`Value ( Quantity * Rate )`)) OVER(),
2
) AS RevenueSharePct
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC;

SELECT
Customer,
SUM(`Value ( Quantity * Rate )`) AS Revenue,
RANK() OVER(
ORDER BY SUM(`Value ( Quantity * Rate )`) DESC
) AS CustomerRank
FROM factsales
GROUP BY Customer;

