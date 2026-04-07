import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import xarray as xr

def load_data(data_dir, variables, scenario, years):
    dfs = []
    for var in variables:
        var_dir = Path(data_dir) / "ACCESS-CM2" / scenario / var
        files = list(var_dir.glob("*.nc"))
        if not files:
            files = [f for f in Path(data_dir).glob("**/*.nc") if f.name.startswith(var) and scenario in str(f)]
        if not files:
            print(f"Warning: No files found for {var} in {scenario}.")
            continue
            
        ds = xr.open_mfdataset(files, use_cftime=True, engine='netcdf4')
        df = ds[var].to_dataframe().reset_index()
        df_time = df.groupby('time')[var].mean().reset_index()
        dfs.append(df_time)

    if not dfs:
        return pd.DataFrame()

    final_df = dfs[0]
    for i in range(1, len(dfs)):
        final_df = final_df.merge(dfs[i], on='time', how='inner')
    return final_df

def main():
    print("Loading historical data...")
    if not os.path.exists("historical_data.csv"):
        print("Required historical_data.csv is missing. Run export_historical.py first.")
        return
        
    hist_df = pd.read_csv("historical_data.csv")
    hist_df.dropna(inplace=True)
    hist_df['time'] = pd.to_datetime(hist_df['time'])

    predictors = ["Relative Humidity (%)", "Average Temperature (°C)", "Wind Speed (m/s)"]
    target = "Precipitation (mm/day)"
    
    X_hist = hist_df[predictors]
    y_hist = hist_df[target]
    
    # Normalize features
    scaler = StandardScaler()
    X_hist_scaled = scaler.fit_transform(X_hist)
    
    # 80-20 Train-Test split for historical validation
    X_train, X_test, y_train, y_test = train_test_split(X_hist_scaled, y_hist, test_size=0.2, random_state=42)

    # 1. Linear Regression Model
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    
    print("\n================ LINEAR REGRESSION ================")
    print("Historical Test R² Score:", f"{r2_score(y_test, lr_pred):.4f}")
    print("Historical Test RMSE:    ", f"{np.sqrt(mean_squared_error(y_test, lr_pred)):.4f}")
    for var, coef in zip(predictors, lr.coef_):
        print(f"  • Weight ({var}): {coef:.6f}")

    # 2. Random Forest Model
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    
    print("\n================ RANDOM FOREST ====================")
    print("Historical Test R² Score:", f"{r2_score(y_test, rf_pred):.4f}")
    print("Historical Test RMSE:    ", f"{np.sqrt(mean_squared_error(y_test, rf_pred)):.4f}")
    for var, imp in zip(predictors, rf.feature_importances_):
        print(f"  • Feature Importance ({var}): {imp:.6f}")
        
    # 3. Load Future Testing datasets
    print("\nLoading future scenario predictors...")
    raw_future_vars = ["hurs", "tas", "sfcWind"]
    future_features = load_data("./data", raw_future_vars, "ssp245", range(2015, 2056))
    
    if future_features.empty:
        print("Could not load future predictor fields!")
        return
        
    # Enforce formatting alignment
    future_features['tas'] = future_features['tas'] - 273.15
    future_features.rename(columns={"hurs": predictors[0], "tas": predictors[1], "sfcWind": predictors[2]}, inplace=True)
    future_features['time'] = pd.to_datetime([str(t) for t in future_features['time']])
    
    print("Loading independently parsed future precipitation truth data...")
    if not os.path.exists("pr_future_data.csv"):
        print("Missing pr_future_data.csv!")
        return
        
    future_target = pd.read_csv("pr_future_data.csv")
    future_target['time'] = pd.to_datetime(future_target['time'])
    
    # Merge future predictors and future target seamlessly
    future_df = future_features.merge(future_target, on='time', how='inner')
    future_df.dropna(inplace=True)
    
    X_future = future_df[predictors]
    y_future_true = future_df[target]
    
    # Scale future data with fit scaler
    X_future_scaled = scaler.transform(X_future)
    
    lr_future_pred = lr.predict(X_future_scaled)
    rf_future_pred = rf.predict(X_future_scaled)
    
    print("\n====== FUTURE (ssp245) VALIDATION METRICS =========")
    print(f"LR R²   : {r2_score(y_future_true, lr_future_pred):.4f}")
    print(f"LR RMSE : {np.sqrt(mean_squared_error(y_future_true, lr_future_pred)):.4f}")
    print(f"RF R²   : {r2_score(y_future_true, rf_future_pred):.4f}")
    print(f"RF RMSE : {np.sqrt(mean_squared_error(y_future_true, rf_future_pred)):.4f}")
    
    # 4. Generate Line Chart visualization of predicted deviations
    plt.figure(figsize=(14, 6))
    
    plt.plot(future_df['time'], y_future_true, label='True GCM Precipitation (Parsed Data)', color='black', alpha=0.8, linewidth=2.0)
    plt.plot(future_df['time'], lr_future_pred, label='Linear Regression Forecast', color='blue', alpha=0.7)
    plt.plot(future_df['time'], rf_future_pred, label='Random Forest Forecast', color='red', alpha=0.7)
    
    plt.title("Model Convergence vs True CMIP6 Precipitation Pattern (ssp245)", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Precipitation (mm/day)", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('future_model_convergence.png', dpi=200)
    print("\nAnalysis chart exported to 'future_model_convergence.png'!")

if __name__ == "__main__":
    main()
