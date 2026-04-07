import pandas as pd
import xarray as xr
from pathlib import Path

def load_historical_var(data_dir, var, years):
    var_dir = Path(data_dir) / "ACCESS-CM2" / "historical" / var
    files = list(var_dir.glob("*.nc"))
    
    if not files:
        files = [f for f in Path(data_dir).glob("**/*.nc") if f.name.startswith(var) and "historical" in str(f)]
        
    if not files:
        print(f"Warning: No historical files found for {var}.")
        return None
        
    ds = xr.open_mfdataset(files, use_cftime=True, engine='netcdf4')
    df = ds[var].to_dataframe().reset_index()
    df_time = df.groupby('time')[var].mean().reset_index()
    return df_time

def main():
    data_dir = "./data"
    variables = ["hurs", "tas", "sfcWind", "pr"]
    years = range(1974, 2015)
    
    dfs = []
    print("Loading historical datasets for CSV export...")
    for var in variables:
        df_var = load_historical_var(data_dir, var, years)
        if df_var is not None and not df_var.empty:
            dfs.append(df_var)
            
    if not dfs:
        print("No historical data available to compose CSV.")
        return

    # Merge all DataFrames along the 'time' column
    hist_df = dfs[0]
    for i in range(1, len(dfs)):
        hist_df = hist_df.merge(dfs[i], on='time', how='inner')
        
    if hist_df.empty:
        print("Merged dataframe is empty.")
        return
        
    hist_df.dropna(inplace=True)
    
    # Optional: Convert cftime objects to readable strings or pandas datetime
    hist_df['time'] = pd.to_datetime([str(t) for t in hist_df['time']])

    print("Applying Conversions...")
    # Convert 'tas' from Kelvin to Celsius
    # Celsius = Kelvin - 273.15
    if 'tas' in hist_df.columns:
        hist_df['tas'] = hist_df['tas'] - 273.15

    # Convert 'pr' from kg m^-2 s^-1 (mm/s) to mm/day
    # mm/day = kg m^-2 s^-1 * 86400 (seconds in a day)
    if 'pr' in hist_df.columns:
        hist_df['pr'] = hist_df['pr'] * 86400

    # Rename columns to clearly state the units
    unit_map = {
        "hurs": "Relative Humidity (%)",
        "tas": "Average Temperature (°C)",
        "sfcWind": "Wind Speed (m/s)",
        "pr": "Precipitation (mm/day)"
    }
    hist_df.rename(columns=unit_map, inplace=True)

    csv_path = "historical_data.csv"
    hist_df.to_csv(csv_path, index=False)
    print(f"Data successfully converted and exported to '{csv_path}'.")

if __name__ == "__main__":
    main()
