import nex_gddp
import xarray as xr
import pandas as pd
from pathlib import Path

def main():
    bbox = (78.136139, 17.160736, 78.730774, 17.618632)
    variables = ["hurs", "tas", "sfcWind"]
    years = list(range(1974, 2015))
    
    print("Downloading data...")
    downloaded_files = nex_gddp.download(
        variables=variables,
        years=years,
        models="ACCESS-CM2",
        scenarios="historical",
        bbox=bbox,
        output_dir="./data"
    )
    
    print(f"Downloaded {len(downloaded_files)} files.")
    
    all_files = list(Path('./data').glob('**/*.nc'))
    if not all_files:
        print("No netcdf files found! Falling back to searching everything in data")
        all_files = list(Path('./data').iterdir())
        print(all_files)
        return

    print("Parsing files...")
    # Open dataset. using cftime is safer for climate model calendars
    try:
        ds = xr.open_mfdataset(all_files, use_cftime=True, engine='netcdf4')
        df = ds.to_dataframe().reset_index()
        
        for var in variables:
            # variables might be capitalized or exactly as listed
            if var in df.columns:
                print(f"\n--- Descriptive statistics for {var} ---")
                print(df[var].describe())
            else:
                print(f"\nVariable '{var}' not found in the dataset. Available columns: {df.columns.tolist()}")

    except Exception as e:
        print(f"Error parsing datasets: {e}")

if __name__ == "__main__":
    main()
