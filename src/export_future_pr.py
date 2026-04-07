import pandas as pd
import xarray as xr
from pathlib import Path

def main():
    # Future projections usually are saved under the SSP scenario folder mapping
    data_dir = Path("./data/ACCESS-CM2/ssp245/pr")
    
    files = list(data_dir.glob("*.nc"))
    
    if not files:
        # Fallback recursive search if directory tree differs
        files = [f for f in Path("./data").glob("**/*.nc") if "pr_" in f.name and "ssp245" in str(f)]
        
    if not files:
        print("No future precipitation (ssp245) files discovered. Please ensure download_pr_and_future.py is complete.")
        return
        
    print(f"Found {len(files)} future precipitation files. Translating to CSV...")
    
    # Aggregate netCDFs dynamically
    ds = xr.open_mfdataset(files, use_cftime=True, engine='netcdf4')
    df = ds['pr'].to_dataframe().reset_index()
    
    # Collapse spatial bounding boxes via geographic average
    df_time = df.groupby('time')['pr'].mean().reset_index()
    
    # Coerce standardized CMIP6 dates to Python Datetimes
    df_time['time'] = pd.to_datetime([str(t) for t in df_time['time']])
    
    # Process mathematical conversion from standard (kg m^-2 s^-1) into (mm/day)
    df_time['pr'] = df_time['pr'] * 86400
    
    df_time.rename(columns={'pr': 'Precipitation (mm/day)'}, inplace=True)
    df_time.dropna(inplace=True)
    
    csv_path = "pr_future_data.csv"
    df_time.to_csv(csv_path, index=False)
    print(f"Future Precipitation Data accurately projected to '{csv_path}'!")

if __name__ == "__main__":
    main()
