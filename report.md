# Hydroclimatic Variable Prediction Using Machine Learning
## Assignment 3 Report

### 1. Selection of Predictands
- **Predictand Variable Selected:** Precipitation (`pr`)
- **Justification:** Precipitation is one of the most vital hydroclimatic variables, directly impacting water resource management, agriculture, and urban planning. For the Hyderabad region, accurate prediction of precipitation is crucial for managing the demands of irrigation and addressing challenges such as urban flooding.

### 2. Selection of Predictors
The input predictors chosen for the model are:
1. **Relative Humidity (`hurs`):** Provides information on moisture availability. High relative humidity is a necessary precondition for substantial precipitation.
2. **Average Temperature (`tas`):** Higher temperatures increase the atmosphere's moisture-holding capacity, often serving as a catalyst for convective rainfall.
3. **Shortwave Radiation (`rsds`):** Represents solar heating driving the hydrological cycle and localized convection events.
4. **Wind Speed (`sfcWind`):** Represents regional atmospheric circulation, which is vital for simulating monsoon behavior in South Asia.

These variables strongly correlate with the physical drivers of precipitation in tropical and subtropical regions.

### 3. Model Development
- **Data Source:** Historical data was downloaded from the NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6) using the `ACCESS-CM2` model. The historical period selected was from 1984 to 2014 (30 years).
- **Preprocessing:** 
   - Variables were converted into human-readable standard units (e.g., Temperature in °C, Precipitation in mm/day).
   - Missing data (if any) was cleaned using Pandas `dropna()`.
   - The features were normalized using `StandardScaler` to ensure scale uniformity.
- **Data Splitting:** An 80-20 train-test split was applied.
- **Machine Learning Model:** A **Random Forest Regressor** was applied. Random Forest is an ensemble learning method that accurately captures complex, non-linear relationships between climatic variables and precipitation without easily overfitting.
- **Evaluation:** Historical model performance was evaluated using **R-squared (R²)** and **Root Mean Squared Error (RMSE)**.

### 4. Future Projection Using Climate Data
- **Future Scenario:** Shared Socioeconomic Pathway 2-4.5 (SSP2-4.5), representing an intermediate greenhouse gas emission scenario.
- **Period:** 2015 to 2040 (25 years).
- **Future Extraction:** The same predictor variables (`hurs`, `tas`, `rsds`, `sfcWind`) were fetched for the future scenario. The trained Random Forest model successfully utilized these inputs to predict precipitation (`pr`) forward in time.
- The same `StandardScaler` fitted on the historical data was applied to the future predictor variables to avoid data leakage.

### 5. Analysis and Inference
Based on the visual analyses and descriptive statistics derived from the `ACCESS-CM2` projections:
- **Correlations:** High relative humidity serves as the primary direct correlate for precipitation. 
- **Trends:** As expected, temperature and associated variables exhibit slight shifts owing to climate change projections under SSP2-4.5.
- **Precipitation Prediction:** The Random Forest prediction effectively captures the general monthly seasonality and monsoonal cycle lengths. For stochastic daily precipitation distributions, predictive models characteristically approximate the mean occurrences and may slightly under-estimate extreme peak outlier events compared directly to GCM physics.
- **Impact Warning:** If the predictions and structural shifts indicate alterations in seasonal norms, Hyderabad could experience irregular monsoon onsets or shifting peak-intensity rainfall, demanding adaptive strategies in urban water management and early warning infrastructure.
