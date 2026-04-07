# Hydro-Assignment 3: Climate Prediction for Hyderabad

This repository contains the data, ML modeling approach, and visual evaluations for predicting hydroclimatic variables (specifically precipitation) in the Hyderabad region. The climate data is sourced from the NEX-GDDP-CMIP6 dataset using the ACCESS-CM2 general circulation model.

## Contents

- **`assignment_3.ipynb`**: The main analytical Jupyter Notebook containing data extraction (via Python API), preprocessing routines, Random Forest model training, validation, and historical/future trend visualization.
- **`report.md`**: Formal assignment report addressing the objective guidelines and explaining the model design and insights.
- **`data/`**: Directory for the raw extracted NetCDF files downloaded from the NEX-GDDP-CMIP6 server (generated upon notebook execution).
- **`historical_data.csv`** & **`future_data.csv`**: Aggregated and structurally merged time-series tables for Model training/prediction.
- **`visualizations/`**: Output charts, feature comparisons, and comparative time-series graphs plotted covering 1984 through 2040.

## Workflow Pipeline

1. **Download:** Automatically pulls subsetted NetCDF datasets matching the bounding box around Hyderabad for the required time periods (Historical: 1984–2014, Future: 2015–2040 SSP2-4.5).
2. **Transform:** Consolidates raw NetCDFs into flat CSVs while standardizing units (e.g. converting `pr` from kg/m²s to mm/day, temperatures to °C).
3. **Train:** A normalized `RandomForestRegressor` acts as the mapping function from predictors `{Humidity, Temperature, Wind Speed, Radiation}` to the target predictand `{Precipitation}`.
4. **Predict:** Generates future point-projections using the trained Random Forest and compares them against GCM physics-simulated expectations under the SSP2-4.5 scenario to identify long-term divergence or pattern tracking.
