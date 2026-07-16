SELECT
SUM(`Value ( Quantity * Rate )`) AS TotalRevenue
FROM factsales;

SELECT
DATE_FORMAT(
STR_TO_DATE(`Date`,'%d-%b-%y'),
'%Y-%m'
) AS Month,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
ORDER BY Month;

SELECT
DATE_FORMAT(
STR_TO_DATE(`Date`, '%d-%b-%y'),
'%Y-%m'
) AS Month,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
HAVING Revenue < 2000000
ORDER BY Month;
