import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    print("Loading historical datasets from CSV...")
    hist_df = pd.read_csv("historical_data.csv")
    hist_df.dropna(inplace=True)
    hist_df['time'] = pd.to_datetime(hist_df['time'])

    print("\n=============================================")
    print("   DESCRIPTIVE STATISTICS (Historical Data)  ")
    print("=============================================\n")
    
    # Columns to analyze and plot
    plot_vars = [
        "Relative Humidity (%)",
        "Average Temperature (°C)",
        "Wind Speed (m/s)",
        "Precipitation (mm/day)"
    ]
    
    stats = hist_df[plot_vars].describe()
    print(stats)
    
    # Save numerical stats directly to a CSV 
    stats.to_csv("historical_descriptive_statistics.csv")
    print("\nDescriptive statistics saved to 'historical_descriptive_statistics.csv'")

    print("\nGenerating visualizations...")
    os.makedirs("visualizations", exist_ok=True)
    
    # 1. Independent Time Series Plots (helps isolate seasonal/decadal trends)
    for var, plot_var in zip(variables, plot_vars):
        plt.figure(figsize=(10, 4))
        plt.plot(hist_df['time'], hist_df[plot_var], label=plot_var, color='teal')
        plt.title(f"Historical Time Series: {plot_var}")
        plt.xlabel("Date")
        plt.ylabel(plot_var)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(f"visualizations/hist_timeseries_{var}.png")
        plt.close()
        
    # 2. Histograms (for viewing data distributions & skewness)
    hist_df[plot_vars].hist(bins=30, figsize=(12, 8), color='coral', edgecolor='black')
    plt.suptitle("Distributions of Historical Variables (1974-2014) with Units", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("visualizations/hist_distributions.png")
    plt.close()

    # 3. Correlation Matrix Plot (for analyzing variable collinearity)
    plt.figure(figsize=(8, 6))
    corr = hist_df[plot_vars].corr()
    plt.matshow(corr, fignum=1, cmap='coolwarm', vmin=-1, vmax=1)
    plt.xticks(range(len(plot_vars)), plot_vars, fontsize=10, rotation=45)
    plt.yticks(range(len(plot_vars)), plot_vars, fontsize=10)
    
    # Annotate correlation coefficient values
    for (i, j), z in np.ndenumerate(corr.values):
        plt.text(j, i, f'{z:0.2f}', ha='center', va='center', color='black' if abs(z) < 0.5 else 'white')
        
    plt.colorbar(label='Pearson Correlation')
    plt.title("Correlation Matrix of Variables", pad=20)
    plt.savefig("visualizations/hist_correlation_matrix.png")
    plt.close()
    
    print("Visualizations successfully compiled and securely saved to the 'visualizations/' directory.")

if __name__ == "__main__":
    main()
