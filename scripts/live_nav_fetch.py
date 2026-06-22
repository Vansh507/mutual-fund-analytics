import requests
import pandas as pd
from pathlib import Path

output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

combined_nav = []

# Loop through all schemes
for fund_label, scheme_code in schemes.items():

    print("=" * 60)
    print(f"Fetching Scheme Code: {scheme_code}")

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)

    if response.status_code != 200:
        print("Request Failed")
        continue

    data = response.json()

    meta = data["meta"]

    print("Fund Name:", meta["scheme_name"])

    nav_df = pd.DataFrame(data["data"])

    # Add metadata
    nav_df["scheme_code"] = meta["scheme_code"]
    nav_df["scheme_name"] = meta["scheme_name"]
    nav_df["fund_house"] = meta["fund_house"]
    nav_df["scheme_category"] = meta["scheme_category"]

    # Safe filename
    filename = (
        meta["scheme_name"]
        .replace("/", "-")
        .replace(" ", "_")
    )

    nav_df.to_csv(
        output_folder / f"{filename}.csv",
        index=False
    )

    combined_nav.append(nav_df)

    print("Saved Successfully")

# Combine all NAV data

all_nav = pd.concat(combined_nav, ignore_index=True)

all_nav.to_csv(
    output_folder / "nav_history.csv",
    index=False
)

print("=" * 60)
print("Combined NAV History Saved")
print(all_nav.shape)