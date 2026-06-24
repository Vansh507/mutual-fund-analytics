CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);





CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE UNIQUE,
    day INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    year INTEGER
);





CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_id INTEGER,
    nav REAL,
    FOREIGN KEY(amfi_code)
        REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date_id)
        REFERENCES dim_date(date_id)
);





CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    amfi_code INTEGER,
    date_id INTEGER,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY(amfi_code)
        REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date_id)
        REFERENCES dim_date(date_id)
);







CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    FOREIGN KEY(amfi_code)
        REFERENCES dim_fund(amfi_code)
);







CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    fund_house TEXT,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    FOREIGN KEY(date_id)
        REFERENCES dim_date(date_id)
);






CREATE TABLE fact_benchmark (
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    index_name TEXT,
    close_value REAL,
    FOREIGN KEY(date_id)
        REFERENCES dim_date(date_id)
);






CREATE TABLE fact_category_inflows (
    inflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    category TEXT,
    net_inflow_crore REAL,
    FOREIGN KEY(date_id)
        REFERENCES dim_date(date_id)
);







CREATE TABLE fact_industry_folios (
    folio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL,
    FOREIGN KEY(date_id)
        REFERENCES dim_date(date_id)
);







CREATE TABLE fact_portfolio_holdings (
    holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    stock_symbol TEXT,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date DATE,
    FOREIGN KEY(amfi_code)
        REFERENCES dim_fund(amfi_code)
);