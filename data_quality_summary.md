# Day 1 Data Quality Summary

## Project
Mutual Fund Analytics Platform

## Data Sources
- AMFI India
- MFAPI

## Datasets Ingested
1. Fund Master
2. Average AUM
3. AMFI Monthly Report
4. NAV History
5. Individual NAV datasets for six schemes

## Data Validation

- Total Schemes in Fund Master: 16,243
- Total AMCs: 54
- Scheme Types: 3
- Scheme Categories: 50

## NAV Validation

- Total Fund Master Codes: 16,243
- Total NAV Codes: 6
- Matching Codes: 6
- Missing Codes: 16,237

## Observations

- Successfully ingested all required datasets.
- NAV history fetched successfully from MFAPI.
- Fund Master contains all AMFI registered schemes.
- NAV history currently includes six schemes fetched for Day 1.
- Duplicate rows observed in the Average AUM dataset.
- No missing values observed in NAV datasets.
- The scheme codes supplied in the internship instructions map to different current schemes in MFAPI, indicating that some reference codes are outdated.