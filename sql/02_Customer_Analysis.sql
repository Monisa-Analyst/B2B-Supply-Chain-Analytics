SELECT
COUNT(DISTINCT Customer) AS TotalCustomers
FROM factsales;

SELECT
Customer,
SUM(`Revenue`) AS Revenue
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC;

SELECT
Customer,
SUM(`Revenue`) AS Revenue
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC
LIMIT 10;

SELECT
Customer,
SUM(`Revenue`) AS Revenue,
ROUND(
SUM(`Value ( Quantity * Rate `)) * 100 /
SUM(SUM(`Revenue`)) OVER(),
2
) AS RevenueSharePct
FROM factsales
GROUP BY Customer
ORDER BY Revenue DESC;

SELECT
Customer,
SUM(`Revenue`) AS Revenue,
RANK() OVER(
ORDER BY SUM(`Revenue`) DESC
) AS CustomerRank
FROM factsales
GROUP BY Customer;

