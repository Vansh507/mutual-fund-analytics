from pathlib import Path
import pandas as pd

raw_folder = Path("data/raw")

print("=" * 80)
print("DATA INGESTION STARTED")
print("=" * 80)

for file in raw_folder.glob("*"):

    # Skip non-data files
    if file.suffix.lower() not in [".csv", ".xls", ".xlsx"]:
        continue

    print("\n" + "=" * 80)
    print(f"Loading File: {file.name}")

    # Read file based on extension
    try:
        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

    except Exception as e:
        print(f"\n❌ Error reading {file.name}")
        print(e)
        continue

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

print("\n")
print("=" * 80)
print("DATA INGESTION COMPLETED")
print("=" * 80)

fund_master = pd.read_csv("data/raw/fund_master.csv")

print(fund_master.columns)

print("\n" + "="*80)
print("FUND MASTER EXPLORATION")
print("="*80)

fund_master = pd.read_csv("data/raw/fund_master.csv")

print("\nTotal Schemes:")
print(fund_master.shape[0])

print("\nTotal Columns:")
print(fund_master.shape[1])

print("\nUnique AMCs:")
print(fund_master["AMC"].nunique())

print("\nAMC Names:")
print(fund_master["AMC"].unique())

print("\nScheme Types:")
print(fund_master["Scheme Type"].unique())

print("\nScheme Categories:")
print(fund_master["Scheme Category"].unique())

print("\n" + "="*80)
print("AMFI CODE VALIDATION")
print("="*80)

nav_history = pd.read_csv("data/raw/nav_history.csv")

master_codes = set(fund_master["Code"])
nav_codes = set(nav_history["scheme_code"])

common_codes = master_codes.intersection(nav_codes)
missing_codes = master_codes - nav_codes

print(f"Total Fund Master Codes : {len(master_codes)}")
print(f"Total NAV Codes         : {len(nav_codes)}")
print(f"Matching Codes          : {len(common_codes)}")
print(f"Missing Codes           : {len(missing_codes)}")