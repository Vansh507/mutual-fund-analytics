# Mutual Fund Analytics - Data Dictionary

## Project Overview

This document describes the structure, data types, and business meaning of all tables used in the Mutual Fund Analytics Data Warehouse. The data warehouse follows a star schema consisting of dimension tables and fact tables.

---

# Dimension Tables

## 1. dim_fund

**Description:** Stores master information for each mutual fund scheme.

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | Unique AMFI code identifying each mutual fund scheme (Primary Key). |
| scheme_name | TEXT | Name of the mutual fund scheme. |
| fund_house | TEXT | Asset Management Company (AMC). |
| category | TEXT | Broad category of the scheme (Equity, Debt, Hybrid, etc.). |
| sub_category | TEXT | Specific sub-category of the scheme. |
| plan | TEXT | Plan type (Direct/Regular). |
| launch_date | DATE | Scheme launch date. |
| benchmark | TEXT | Benchmark index used for comparison. |
| expense_ratio_pct | REAL | Annual expense ratio charged by the fund. |
| exit_load_pct | REAL | Exit load percentage charged on redemption. |
| min_sip_amount | REAL | Minimum SIP investment amount. |
| min_lumpsum_amount | REAL | Minimum lump sum investment amount. |
| fund_manager | TEXT | Name of the fund manager. |
| risk_category | TEXT | Risk level of the scheme. |
| sebi_category_code | TEXT | SEBI category code. |

---

## 2. dim_date

**Description:** Date dimension used by all fact tables.

| Column | Data Type | Description |
|---------|-----------|-------------|
| date_id | INTEGER | Surrogate primary key. |
| full_date | DATE | Calendar date. |
| day | INTEGER | Day of month. |
| month | INTEGER | Month number (1–12). |
| month_name | TEXT | Month name. |
| quarter | INTEGER | Quarter (1–4). |
| year | INTEGER | Calendar year. |

---

# Fact Tables

## 3. fact_nav

**Description:** Historical Net Asset Value (NAV) records.

| Column | Data Type | Description |
|---------|-----------|-------------|
| nav_id | INTEGER | Primary Key. |
| amfi_code | INTEGER | References dim_fund. |
| date_id | INTEGER | References dim_date. |
| nav | REAL | Daily Net Asset Value. |

---

## 4. fact_transactions

**Description:** Investor transaction records.

| Column | Data Type | Description |
|---------|-----------|-------------|
| transaction_id | INTEGER | Primary Key. |
| investor_id | TEXT | Unique investor identifier. |
| amfi_code | INTEGER | Mutual fund scheme code. |
| date_id | INTEGER | Transaction date. |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption. |
| amount_inr | REAL | Transaction amount in INR. |
| state | TEXT | Investor state. |
| city | TEXT | Investor city. |
| city_tier | TEXT | City classification (Tier 1, Tier 2, etc.). |
| age_group | TEXT | Investor age group. |
| gender | TEXT | Investor gender. |
| annual_income_lakh | REAL | Annual income (Lakhs). |
| payment_mode | TEXT | Mode of payment. |
| kyc_status | TEXT | Investor KYC verification status. |

---

## 5. fact_performance

**Description:** Performance metrics of mutual fund schemes.

| Column | Data Type | Description |
|---------|-----------|-------------|
| performance_id | INTEGER | Primary Key. |
| amfi_code | INTEGER | References dim_fund. |
| return_1yr_pct | REAL | One-year return (%). |
| return_3yr_pct | REAL | Three-year return (%). |
| return_5yr_pct | REAL | Five-year return (%). |
| benchmark_3yr_pct | REAL | Benchmark 3-year return. |
| alpha | REAL | Alpha performance measure. |
| beta | REAL | Beta value. |
| sharpe_ratio | REAL | Sharpe Ratio. |
| sortino_ratio | REAL | Sortino Ratio. |
| std_dev_ann_pct | REAL | Annualized standard deviation. |
| max_drawdown_pct | REAL | Maximum drawdown percentage. |
| aum_crore | REAL | Assets Under Management (Crores). |
| expense_ratio_pct | REAL | Expense ratio (%). |
| morningstar_rating | INTEGER | Morningstar rating. |
| risk_grade | TEXT | Overall risk grade. |

---

## 6. fact_aum

**Description:** Assets Under Management by fund house.

| Column | Data Type | Description |
|---------|-----------|-------------|
| aum_id | INTEGER | Primary Key. |
| date_id | INTEGER | References dim_date. |
| fund_house | TEXT | Asset Management Company. |
| aum_lakh_crore | REAL | AUM in lakh crores. |
| aum_crore | REAL | AUM in crores. |
| num_schemes | INTEGER | Number of schemes managed. |

---

## 7. fact_benchmark

**Description:** Historical benchmark index values.

| Column | Data Type | Description |
|---------|-----------|-------------|
| benchmark_id | INTEGER | Primary Key. |
| date_id | INTEGER | References dim_date. |
| index_name | TEXT | Benchmark index name. |
| close_value | REAL | Closing index value. |

---

## 8. fact_category_inflows

**Description:** Monthly net inflows by mutual fund category.

| Column | Data Type | Description |
|---------|-----------|-------------|
| inflow_id | INTEGER | Primary Key. |
| date_id | INTEGER | References dim_date. |
| category | TEXT | Mutual fund category. |
| net_inflow_crore | REAL | Net inflow amount (Crores). |

---

## 9. fact_industry_folios

**Description:** Monthly industry-wide folio statistics.

| Column | Data Type | Description |
|---------|-----------|-------------|
| folio_id | INTEGER | Primary Key. |
| date_id | INTEGER | References dim_date. |
| total_folios_crore | REAL | Total investor folios (Crores). |
| equity_folios_crore | REAL | Equity fund folios. |
| debt_folios_crore | REAL | Debt fund folios. |
| hybrid_folios_crore | REAL | Hybrid fund folios. |
| others_folios_crore | REAL | Other category folios. |

---

## 10. fact_portfolio_holdings

**Description:** Portfolio holdings of mutual fund schemes.

| Column | Data Type | Description |
|---------|-----------|-------------|
| holding_id | INTEGER | Primary Key. |
| amfi_code | INTEGER | References dim_fund. |
| stock_symbol | TEXT | Stock ticker symbol. |
| stock_name | TEXT | Company name. |
| sector | TEXT | Industry sector. |
| weight_pct | REAL | Portfolio weight (%). |
| market_value_cr | REAL | Market value (Crores). |
| current_price_inr | REAL | Current stock price (INR). |
| portfolio_date | DATE | Portfolio reporting date. |

---

# Data Sources

| Dataset | Purpose |
|---------|----------|
| fund_master_cleaned.csv | Mutual fund master information |
| nav_history_cleaned.csv | Historical NAV data |
| investor_transactions_cleaned.csv | Investor transaction history |
| scheme_performance_cleaned.csv | Scheme performance metrics |
| aum_by_fund_house_cleaned.csv | Assets under management |
| benchmark_indices_cleaned.csv | Benchmark index history |
| category_inflows_cleaned.csv | Category-wise inflows |
| industry_folio_count_cleaned.csv | Industry folio statistics |
| portfolio_holdings_cleaned.csv | Portfolio holdings |

---

# Database Summary

- Database: SQLite
- Schema Design: Star Schema
- Dimension Tables: 2
- Fact Tables: 8
- Total Tables: 10
- Total Records Loaded: ~88,000+