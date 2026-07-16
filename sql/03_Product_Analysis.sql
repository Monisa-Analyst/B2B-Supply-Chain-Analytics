SELECT
Products,
SUM(`Revenue`) AS Revenue
FROM factsales
GROUP BY Products
ORDER BY Revenue DESC;

SELECT
Products,
SUM(`Revenue`) AS Revenue
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
SUM(`Revenue`) AS Revenue,
RANK() OVER(
ORDER BY SUM(`Revenue`) DESC
) AS ProductRank
FROM factsales
GROUP BY Products;



