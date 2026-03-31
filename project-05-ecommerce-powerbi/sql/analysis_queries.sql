q1 = """
SELECT 
    p.category,
    COUNT(DISTINCT f.order_id)      AS total_orders,
    ROUND(SUM(f.sales), 2)          AS total_sales,
    ROUND(SUM(f.profit), 2)         AS total_profit,
    ROUND(AVG(f.profit_margin), 2)  AS avg_profit_margin
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC
"""
df_q1 = run_query(q1)
print(df_q1)

q2 = """
SELECT 
    l.region,
    c.segment,
    ROUND(SUM(f.sales), 2)    AS total_sales,
    ROUND(SUM(f.profit), 2)   AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_orders f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_location  l ON f.postal_code  = l.postal_code
GROUP BY l.region, c.segment
ORDER BY l.region, total_sales DESC
"""
df_q2 = run_query(q2)
print(df_q2)

q3 = """
SELECT 
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2)         AS total_sales,
    ROUND(SUM(f.profit), 2)        AS total_profit,
    ROUND(AVG(f.profit_margin), 2) AS avg_margin,
    SUM(f.quantity)                AS units_sold
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_name, p.category, p.sub_category
ORDER BY total_profit DESC
LIMIT 10
"""
df_q3 = run_query(q3)
print(df_q3)

q4 = """
SELECT 
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.profit), 2)        AS total_profit,
    ROUND(AVG(f.discount), 2)      AS avg_discount,
    ROUND(AVG(f.profit_margin), 2) AS avg_margin,
    COUNT(*)                       AS order_count
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_name, p.category, p.sub_category
HAVING total_profit < 0
ORDER BY total_profit ASC
LIMIT 10
"""
df_q4 = run_query(q4)
print(df_q4)

q5 = """
SELECT 
    order_year,
    order_month,
    ROUND(SUM(sales), 2)   AS monthly_sales,
    ROUND(SUM(profit), 2)  AS monthly_profit,
    COUNT(DISTINCT order_id) AS orders
FROM fact_orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month
"""
df_q5 = run_query(q5)
print(df_q5.head(20))

q6 = """
SELECT 
    c.customer_name,
    c.segment,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders,
    RANK() OVER (ORDER BY SUM(f.sales) DESC) AS sales_rank
FROM fact_orders f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_name, c.segment
ORDER BY sales_rank
LIMIT 15
"""
df_q6 = run_query(q6)
print(df_q6)

q7 = """
SELECT 
    s.ship_mode,
    COUNT(*) AS total_shipments,
    ROUND(AVG(f.shipping_days), 1) AS avg_ship_days,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM fact_orders f
JOIN dim_shipping s ON f.order_id = s.order_id
GROUP BY s.ship_mode
ORDER BY avg_ship_days
"""
df_q7 = run_query(q7)
print(df_q7)

q8 = """
SELECT 
    CASE 
        WHEN discount = 0         THEN 'No Discount'
        WHEN discount <= 0.10     THEN 'Low (1-10%)'
        WHEN discount <= 0.30     THEN 'Medium (11-30%)'
        WHEN discount <= 0.50     THEN 'High (31-50%)'
        ELSE 'Very High (50%+)'
    END AS discount_tier,
    COUNT(*) AS order_count,
    ROUND(AVG(profit_margin), 2) AS avg_profit_margin,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM fact_orders
GROUP BY discount_tier
ORDER BY avg_profit_margin DESC
"""
df_q8 = run_query(q8)
print(df_q8)

q9 = """
SELECT 
    l.state,
    l.region,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(AVG(f.profit_margin), 2) AS avg_margin
FROM fact_orders f
JOIN dim_location l ON f.postal_code = l.postal_code
GROUP BY l.state, l.region
ORDER BY total_sales DESC
LIMIT 15
"""
df_q9 = run_query(q9)
print(df_q9)

q10 = """
WITH quarterly_sales AS (
    SELECT 
        order_year,
        order_quarter,
        ROUND(SUM(sales), 2) AS quarterly_sales,
        ROUND(SUM(profit), 2) AS quarterly_profit
    FROM fact_orders
    GROUP BY order_year, order_quarter
)
SELECT 
    order_year,
    order_quarter,
    quarterly_sales,
    quarterly_profit,
    LAG(quarterly_sales) OVER (ORDER BY order_year, order_quarter) AS prev_quarter_sales,
    ROUND((quarterly_sales - LAG(quarterly_sales) 
        OVER (ORDER BY order_year, order_quarter)) 
        / LAG(quarterly_sales) 
        OVER (ORDER BY order_year, order_quarter) * 100, 2) AS qoq_growth_pct
FROM quarterly_sales
ORDER BY order_year, order_quarter
"""
df_q10 = run_query(q10)
print(df_q10)