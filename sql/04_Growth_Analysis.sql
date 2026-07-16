WITH MonthlyRevenue AS
(
SELECT
DATE_FORMAT(
STR_TO_DATE(`Date`,'%d-%b-%y'),
'%Y-%m'
) AS Month,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
)

SELECT
Month,
Revenue,
LAG(Revenue) OVER(
ORDER BY Month
) AS PrevRevenue
FROM MonthlyRevenue;

WITH MonthlyRevenue AS
(
SELECT
DATE_FORMAT(
STR_TO_DATE(`Date`,'%d-%b-%y'),
'%Y-%m'
) AS Month,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
)

SELECT
Month,
Revenue,
LAG(Revenue) OVER(
ORDER BY Month
) AS PrevRevenue,
ROUND(
(Revenue -
LAG(Revenue) OVER(ORDER BY Month))
/
LAG(Revenue) OVER(ORDER BY Month)
*100,
2
) AS GrowthPct
FROM MonthlyRevenue;

WITH MonthlyRevenue AS
(
SELECT
DATE_FORMAT(
STR_TO_DATE(`Date`,'%d-%b-%y'),
'%Y-%m'
) AS Month,
SUM(`Value ( Quantity * Rate )`) AS Revenue
FROM factsales
GROUP BY Month
)

SELECT
Month,
Revenue,
SUM(Revenue)
OVER(
ORDER BY Month
) AS RunningRevenue
FROM MonthlyRevenue;