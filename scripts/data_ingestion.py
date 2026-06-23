from pathlib import Path
import pandas as pd

raw_folder = Path("data/raw")

print("=" * 80)
print("DATA INGESTION STARTED")
print("=" * 80)

for file in sorted(raw_folder.glob("*.csv")):

    print("\n" + "=" * 80)
    print(f"Loading File: {file.name}")

    try:
        df = pd.read_csv(file)

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

    except Exception as e:
        print(f"Error reading {file.name}")
        print(e)

print("\n" + "=" * 80)
print("DATA INGESTION COMPLETED")
print("=" * 80)