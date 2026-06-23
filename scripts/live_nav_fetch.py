import requests
import pandas as pd
from pathlib import Path

output_folder = Path("data/raw/live_nav")
output_folder.mkdir(parents=True, exist_ok=True)

schemes = {
    "HDFC Top 100": 125497,
    "SBI Bluechip": 119551,
    "ICICI Bluechip": 120503,
    "Nippon Large Cap": 118632,
    "Axis Bluechip": 119092,
    "Kotak Bluechip": 120841
}

combined_nav = []

# Fetch live NAV for all schemes
for scheme_name, scheme_code in schemes.items():

    print("=" * 70)
    print(f"Fetching: {scheme_name}")

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch {scheme_name}")
        continue

    data = response.json()

    # Convert NAV history to DataFrame
    nav_df = pd.DataFrame(data["data"])

    # Add metadata
    nav_df["scheme_code"] = data["meta"]["scheme_code"]
    nav_df["scheme_name"] = data["meta"]["scheme_name"]
    nav_df["fund_house"] = data["meta"]["fund_house"]
    nav_df["scheme_category"] = data["meta"]["scheme_category"]

    # Create a safe filename
    file_name = (
        scheme_name
        .replace(" ", "_")
        .replace("/", "_")
        + ".csv"
    )

    nav_df.to_csv(output_folder / file_name, index=False)

    combined_nav.append(nav_df)

    print(f"Saved: {file_name}")

# Combine all downloaded NAV data
all_nav = pd.concat(combined_nav, ignore_index=True)

all_nav.to_csv(output_folder / "live_nav_all.csv", index=False)

print("\n" + "=" * 70)
print("Live NAV fetch completed successfully!")
print(f"Total Records: {all_nav.shape[0]}")