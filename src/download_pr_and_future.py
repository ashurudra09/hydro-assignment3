import nex_gddp
from pathlib import Path

def main():
    bbox = (78.136139, 17.160736, 78.730774, 17.618632)
    
    # 1. Download historical precipitation (pr)
    print("Downloading historical precipitation (1974-2014)...")
    nex_gddp.download(
        variables=["pr"],
        years=list(range(1974, 2015)),
        models="ACCESS-CM2",
        scenarios="historical",
        bbox=bbox,
        output_dir="./data",
        max_workers=1
    )
    
    # 2. Download future data (all variables) for scenario ssp245
    print("Downloading future predictions (2015-2055) for scenario ssp245...")
    nex_gddp.download(
        variables=["pr"],
        years=list(range(2015, 2056)),
        models="ACCESS-CM2",
        scenarios="ssp245",  # We default to the moderate emissions scenario
        bbox=bbox,
        output_dir="./data",
        max_workers=1
    )

    print("All downloads completed successfully.")

if __name__ == "__main__":
    main()
