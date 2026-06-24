from pathlib import Path
import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, inspect, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SQL_FOLDER = PROJECT_ROOT / "sql"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

DATABASE_PATH = PROJECT_ROOT / "bluestock_mf.db"


if DATABASE_PATH.exists():
    os.remove(DATABASE_PATH)
    print("Old database deleted.")


engine = create_engine(f"sqlite:///{DATABASE_PATH}")

print("Database created successfully!")


conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

with open(SQL_FOLDER / "schema.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Schema created successfully!")


inspector = inspect(engine)

print("\nTables Created:")

for table in inspector.get_table_names():
    print(f"created {table}")


def load_csv(filename):

    df = pd.read_csv(PROCESSED_DATA / filename)

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df


def get_date_lookup():

    dim_date = pd.read_sql(
        "SELECT date_id, full_date FROM dim_date",
        engine
    )

    dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])

    return dim_date


def load_dim_fund():

    print("\nLoading dim_fund...")

    fund_master = load_csv("fund_master_cleaned.csv")

    fund_master.to_sql(
        "dim_fund",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fund_master)} rows.")

def load_dim_date():

    print("\nLoading dim_date...")

    nav = load_csv("nav_history_cleaned.csv")
    transactions = load_csv("investor_transactions_cleaned.csv")
    benchmark = load_csv("benchmark_indices_cleaned.csv")
    sip = load_csv("monthly_sip_inflows_cleaned.csv")
    aum = load_csv("aum_by_fund_house_cleaned.csv")

    all_dates = pd.concat([

        pd.to_datetime(nav["date"]),

        pd.to_datetime(transactions["transaction_date"]),

        pd.to_datetime(benchmark["date"]),

        pd.to_datetime(sip["month"]),

        pd.to_datetime(aum["date"])

    ])

    all_dates = (
        pd.Series(all_dates.unique())
        .sort_values()
        .reset_index(drop=True)
    )

    dim_date = pd.DataFrame()

    dim_date["full_date"] = all_dates

    dim_date["day"] = dim_date["full_date"].dt.day

    dim_date["month"] = dim_date["full_date"].dt.month

    dim_date["month_name"] = dim_date["full_date"].dt.month_name()

    dim_date["quarter"] = dim_date["full_date"].dt.quarter

    dim_date["year"] = dim_date["full_date"].dt.year

    dim_date.to_sql(
        "dim_date",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(dim_date)} rows.")



def load_fact_nav():

    print("\nLoading fact_nav...")

    nav = load_csv("nav_history_cleaned.csv")

    nav["date"] = pd.to_datetime(nav["date"])

    date_lookup = get_date_lookup()

    nav = nav.merge(
        date_lookup,
        left_on="date",
        right_on="full_date",
        how="left"
    )

    fact_nav = nav[
        [
            "amfi_code",
            "date_id",
            "nav"
        ]
    ]

    fact_nav.to_sql(
        "fact_nav",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_nav)} rows.")


def load_fact_transactions():

    print("\nLoading fact_transactions...")

    transactions = load_csv("investor_transactions_cleaned.csv")

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"]
    )

    date_lookup = get_date_lookup()

    transactions = transactions.merge(
        date_lookup,
        left_on="transaction_date",
        right_on="full_date",
        how="left"
    )

    fact_transactions = transactions[
        [
            "investor_id",
            "amfi_code",
            "date_id",
            "transaction_type",
            "amount_inr",
            "state",
            "city",
            "city_tier",
            "age_group",
            "gender",
            "annual_income_lakh",
            "payment_mode",
            "kyc_status"
        ]
    ]

    fact_transactions.to_sql(
        "fact_transactions",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_transactions)} rows.")


def load_fact_performance():

    print("\nLoading fact_performance...")

    performance = load_csv("scheme_performance_cleaned.csv")

    fact_performance = performance[
        [
            "amfi_code",
            "return_1yr_pct",
            "return_3yr_pct",
            "return_5yr_pct",
            "benchmark_3yr_pct",
            "alpha",
            "beta",
            "sharpe_ratio",
            "sortino_ratio",
            "std_dev_ann_pct",
            "max_drawdown_pct",
            "aum_crore",
            "expense_ratio_pct",
            "morningstar_rating",
            "risk_grade"
        ]
    ]

    fact_performance.to_sql(
        "fact_performance",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_performance)} rows.")



def load_fact_aum():

    print("\nLoading fact_aum...")

    aum = load_csv("aum_by_fund_house_cleaned.csv")

    aum["date"] = pd.to_datetime(aum["date"])

    date_lookup = get_date_lookup()

    aum = aum.merge(
        date_lookup,
        left_on="date",
        right_on="full_date",
        how="left"
    )

    fact_aum = aum[
        [
            "date_id",
            "fund_house",
            "aum_lakh_crore",
            "aum_crore",
            "num_schemes"
        ]
    ]

    fact_aum.to_sql(
        "fact_aum",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_aum)} rows.")


def load_fact_benchmark():

    print("\nLoading fact_benchmark...")

    benchmark = load_csv("benchmark_indices_cleaned.csv")

    benchmark["date"] = pd.to_datetime(benchmark["date"])

    date_lookup = get_date_lookup()

    benchmark = benchmark.merge(
        date_lookup,
        left_on="date",
        right_on="full_date",
        how="left"
    )

    fact_benchmark = benchmark[
        [
            "date_id",
            "index_name",
            "close_value"
        ]
    ]

    fact_benchmark.to_sql(
        "fact_benchmark",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_benchmark)} rows.")


def load_fact_category_inflows():

    print("\nLoading fact_category_inflows...")

    category = load_csv("category_inflows_cleaned.csv")

    category["month"] = pd.to_datetime(category["month"])

    date_lookup = get_date_lookup()

    category = category.merge(
        date_lookup,
        left_on="month",
        right_on="full_date",
        how="left"
    )

    fact_category = category[
        [
            "date_id",
            "category",
            "net_inflow_crore"
        ]
    ]

    fact_category.to_sql(
        "fact_category_inflows",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_category)} rows.")


def load_fact_industry_folios():

    print("\nLoading fact_industry_folios...")

    folio = load_csv("industry_folio_count_cleaned.csv")

    folio["month"] = pd.to_datetime(folio["month"])

    date_lookup = get_date_lookup()

    folio = folio.merge(
        date_lookup,
        left_on="month",
        right_on="full_date",
        how="left"
    )

    fact_folio = folio[
        [
            "date_id",
            "total_folios_crore",
            "equity_folios_crore",
            "debt_folios_crore",
            "hybrid_folios_crore",
            "others_folios_crore"
        ]
    ]

    fact_folio.to_sql(
        "fact_industry_folios",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_folio)} rows.")


def load_fact_portfolio_holdings():

    print("\nLoading fact_portfolio_holdings...")

    holdings = load_csv("portfolio_holdings_cleaned.csv")

    fact_holdings = holdings[
        [
            "amfi_code",
            "stock_symbol",
            "stock_name",
            "sector",
            "weight_pct",
            "market_value_cr",
            "current_price_inr",
            "portfolio_date"
        ]
    ]

    fact_holdings.to_sql(
        "fact_portfolio_holdings",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(fact_holdings)} rows.")


def verify_database():

    print("\n" + "=" * 50)
    print("DATABASE LOADING SUMMARY")
    print("=" * 50)

    tables = inspect(engine).get_table_names()

    for table in tables:

        rows = pd.read_sql(
            f"SELECT COUNT(*) AS total FROM {table}",
            engine
        ).iloc[0]["total"]

        print(f"{table:<30} {rows}")

    print("=" * 50)
    print("Database loaded successfully.")



if __name__ == "__main__":

    load_dim_fund()

    load_dim_date()

    load_fact_nav()

    load_fact_transactions()

    load_fact_performance()

    load_fact_aum()

    load_fact_benchmark()

    load_fact_category_inflows()

    load_fact_industry_folios()

    load_fact_portfolio_holdings()

    verify_database()

    print("\nETL Pipeline Completed Successfully!")