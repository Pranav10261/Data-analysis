
SELECT * FROM sales.superstore_cleaned;


SELECT ROUND(SUM(sales), 2) AS total_sales,
ROUND(SUM(profit), 2) AS total_profit,
ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct,
COUNT(DISTINCT order_id) AS order_count
FROM sales.superstore_cleaned;

SELECT
    ship_mode,
    ROUND(AVG(shipping_cost), 2) AS avg_shipcost
FROM sales.superstore_cleaned
GROUP BY ship_mode
ORDER BY avg_shipcost DESC;


SELECT
    FLOOR(discount * 10) / 10 AS discount_bin,
    ROUND(SUM(profit), 2)  AS total_profit
FROM sales.superstore_cleaned
GROUP BY discount_bin
ORDER BY discount_bin;


SELECT year,QUARTER(order_date)  AS quarter,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales.superstore_cleaned
GROUP BY year, quarter
ORDER BY year, quarter;

SELECT
    country,
    market,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales.superstore_cleaned
GROUP BY country, market
ORDER BY total_sales DESC;



SELECT
    category,
    sub_category,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales.superstore_cleaned
GROUP BY category, sub_category
ORDER BY category, total_profit DESC;



SELECT
    category,
    FLOOR(discount * 10) / 10  AS discount_bin,
    ROUND(SUM(sales * discount / NULLIF(1 - discount, 0)), 2)  AS discount_impact,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)  AS profit_margin_pct
FROM sales.superstore_cleaned
GROUP BY category, discount_bin
ORDER BY category, discount_bin;



SELECT
    segment,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct
FROM sales.superstore_cleaned
GROUP BY segment
ORDER BY profit_margin_pct DESC;



SELECT
    country,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales), 2)  AS total_sales
FROM sales.superstore_cleaned
GROUP BY country
ORDER BY country;



SELECT
    customer_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales.superstore_cleaned
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 20;