import nex_gddp

def main():
    bbox = (78.136139, 17.160736, 78.730774, 17.618632)
    print("Downloading missing future predictors (hurs, tas, sfcWind) for scenario ssp245 (2015-2055)...")
    nex_gddp.download(
        variables=["hurs", "tas", "sfcWind"],
        years=list(range(2015, 2056)),
        models="ACCESS-CM2",
        scenarios="ssp245",
        bbox=bbox,
        output_dir="./data",
        max_workers=1
    )

if __name__ == "__main__":
    main()
