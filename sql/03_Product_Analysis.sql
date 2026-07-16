SELECT
Products,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Products
ORDER BY Revenue DESC;

SELECT
Products,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Products
ORDER BY Revenue DESC
LIMIT 10;

SELECT
Products,
SUM(Quantity) AS UnitsSold
FROM factsales
GROUP BY Products
ORDER BY UnitsSold DESC;

SELECT
Products,
SUM(`Value ( Quantity * Rate )`) AS Revenue,
RANK() OVER(
ORDER BY SUM(`Value ( Quantity * Rate )`) DESC
) AS ProductRank
FROM factsales
GROUP BY Products;



