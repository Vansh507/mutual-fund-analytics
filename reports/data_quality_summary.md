# Day 1 Data Quality Summary
## Project

-Mutual Fund Analytics Platform
-Bluestock Fintech Internship Capstone Project

## Objective

The objective of Day 1 was to establish the project structure, ingest the provided datasets, fetch live NAV data from MFAPI, perform initial data validation, and prepare the project for further ETL processing.

## Datasets Ingested

The following datasets were successfully loaded into the project:

-fund_master.csv	
-nav_history.csv	
-aum_by_fund_house.csv	
-monthly_sip_inflows.csv
-category_inflows.csv
-industry_folio_count.csv
-scheme_performance.csv
-investor_transactions.csv
-portfolio_holdings.csv
-benchmark_indices.csv

In addition to the provided datasets, live NAV data for six mutual fund schemes was successfully fetched from the MFAPI and stored separately under the data/raw/live_nav/ directory.

## Data Validation Performed

The following validation checks were performed on all datasets:

-Dataset dimensions (rows and columns)
-Data types
-Sample records using .head()
-Missing value analysis
-Duplicate record analysis

## Data Quality Results

Fund Master Dataset

-Total Records: 40
-Total Columns: 15
-Missing Values: 0
-Duplicate Rows: 0

## NAV History Dataset

-Total Records: 46,000
-Total Columns: 3
-Missing Values: 0
-Duplicate Rows: 0

## AMFI Code Validation

The AMFI scheme codes were validated between the Fund Master and NAV History datasets.

-Validation Metric:	  Count
-Fund Master Codes:	    40
-NAV History Codes:	    40
-Matching Codes:	    40
-Missing Codes:	         0

All scheme codes from the Fund Master were successfully found in the NAV History dataset, confirming complete consistency between the provided datasets.

## Live NAV Integration

A separate Python script (live_nav_fetch.py) was developed to connect to the MFAPI and retrieve live NAV history for the required mutual fund schemes.

The script:

-Connected successfully to the MFAPI.
-Retrieved live NAV data.
-Converted JSON responses into Pandas DataFrames.
-Saved individual scheme CSV files.
-Generated a consolidated live_nav_all.csv dataset.

## Observations

-All provided datasets were successfully loaded without errors.
-No missing values were detected in the Fund Master and NAV History datasets.
-No duplicate records were found in the validated datasets.
-All AMFI codes matched successfully between the Fund Master and NAV History datasets.
-Live NAV data was successfully retrieved and stored separately from the provided historical datasets to -maintain a clear distinction between static and live data sources.

## Conclusion

Day 1 objectives were successfully completed. The project environment, folder structure, GitHub repository, data ingestion scripts, and live NAV integration have been established. The raw datasets have been validated and are ready for the data cleaning, preprocessing, and database loading stages in the next phase of the project.