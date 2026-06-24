-- 1. Top 5 Funds by AUM
SELECT
    fp.amfi_code,
    df.scheme_name,
    df.fund_house,
    fp.aum_crore
FROM fact_performance fp
JOIN dim_fund df
ON fp.amfi_code = df.amfi_code
ORDER BY fp.aum_crore DESC
LIMIT 5;



-- 2. Average NAV per Month
SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav),2) AS average_nav
FROM fact_nav n
JOIN dim_date d
ON n.date_id = d.date_id
GROUP BY d.year,d.month
ORDER BY d.year,d.month;




-- 3. Transactions by State
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;



-- 4. Funds with Expense Ratio < 1%
SELECT
    df.scheme_name,
    df.fund_house,
    fp.expense_ratio_pct
FROM fact_performance fp
JOIN dim_fund df
ON fp.amfi_code = df.amfi_code
WHERE fp.expense_ratio_pct < 1
ORDER BY fp.expense_ratio_pct;




-- 5. Average 3-Year Return by Category
SELECT
    category,
    ROUND(AVG(return_3yr_pct),2) AS avg_return
FROM fact_performance fp
JOIN dim_fund df
ON fp.amfi_code=df.amfi_code
GROUP BY category
ORDER BY avg_return DESC;




-- 6. Top 10 Funds by 5-Year Return
SELECT
    scheme_name,
    return_5yr_pct
FROM fact_performance fp
JOIN dim_fund df
ON fp.amfi_code=df.amfi_code
ORDER BY return_5yr_pct DESC
LIMIT 10;




-- 7. Total AUM by Fund House
SELECT
    fund_house,
    ROUND(SUM(aum_crore),2) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC;




-- 8. Monthly Category Inflows
SELECT
    d.year,
    d.month,
    ROUND(SUM(net_inflow_crore),2) AS total_inflow
FROM fact_category_inflows c
JOIN dim_date d
ON c.date_id=d.date_id
GROUP BY d.year,d.month
ORDER BY d.year, d.month;




-- 9. Portfolio Holdings by Sector
SELECT
    sector,
    COUNT(*) AS stocks,
    ROUND(AVG(weight_pct),2) AS avg_weight
FROM fact_portfolio_holdings
GROUP BY sector
ORDER BY stocks DESC;




-- 10. Highest NAV Recorded
SELECT
    scheme_name,
    MAX(nav) AS highest_nav
FROM fact_nav n
JOIN dim_fund d
ON n.amfi_code=d.amfi_code
GROUP BY scheme_name
ORDER BY highest_nav DESC
LIMIT 10;