import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re

INPUT_FILE = "market_analysis/integra_market_data.csv"
OUTPUT_PLOT_FILE = "market_analysis/price_trends.png"
SUMMARY_FILE = "market_analysis/market_summary.md"

def clean_price(price_str):
    if not isinstance(price_str, str): return None
    # "200.0万円" -> 2000000, "---" -> None
    # Sometimes it has commas
    if "---" in price_str: return None
    
    # Remove '万円', '円', commas, whitespace
    clean = re.sub(r'[万円,]', '', price_str).strip()
    try:
        val = float(clean)
        return int(val * 10000)
    except ValueError:
        return None

def clean_year(year_str):
    # "2001(H13)" -> 2001
    if not isinstance(year_str, str): return None
    match = re.match(r'(\d{4})', year_str)
    if match:
        return int(match.group(1))
    return None

def clean_mileage(mile_str):
    # "5.4万km" -> 54000, "1000km" -> 1000, "---" -> None
    if not isinstance(mile_str, str): return None
    if "---" in mile_str or "?" in mile_str: return None
    
    clean = mile_str.replace(",", "").replace("km", "").strip()
    try:
        if "万" in clean:
            val = float(clean.replace("万", ""))
            return int(val * 10000)
        else:
            return int(float(clean))
    except ValueError:
        return None

def main():
    print("Loading data...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Run scraper.py first.")
        return

    # Cleaning
    print("Cleaning data...")
    df['Price'] = df['Total_Price_Raw'].apply(clean_price)
    # If Total Price is missing, fall back to Base Price? 
    # Usually we want Total Price for analysis, but Base is okay if Total is missing.
    # Let's stick to Total Price primarily, or make a combined column.
    # For now, let's just use cleaned Total Price for simplicity, assuming most have it.
    
    # Fallback to base price if total is null
    mask_null_total = df['Price'].isnull()
    df.loc[mask_null_total, 'Price'] = df.loc[mask_null_total, 'Base_Price_Raw'].apply(clean_price)
    
    df['Year'] = df['Year_Raw'].apply(clean_year)
    df['Mileage_km'] = df['Mileage_Raw'].apply(clean_mileage)

    # Filter out invalid rows for plotting
    plot_df = df.dropna(subset=['Price', 'Year'])
    
    print(f"Valid data points for plotting: {len(plot_df)}")
    
    if len(plot_df) == 0:
        print("No valid data to plot.")
        return

    # Visualization
    print("Generating plot...")
    plt.figure(figsize=(12, 8))
    
    # Separate by Type R vs Regular
    # Our scraper sets Model_Group to "Integra" or "Integra Type R"
    groups = plot_df.groupby('Model_Group')
    
    for name, group in groups:
        plt.scatter(group['Year'], group['Price'], label=name, alpha=0.7, edgecolors='w', s=60)
        
    plt.title('Used Honda Integra Price Trends', fontsize=16)
    plt.xlabel('Model Year', fontsize=12)
    plt.ylabel('Price (JPY)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # Format Y axis as currency
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT_FILE)
    print(f"Plot saved to {OUTPUT_PLOT_FILE}")

    # Summary Statistics
    summary = plot_df.groupby('Model_Group')['Price'].agg(['count', 'mean', 'min', 'max']).round(0)
    
    # Generate Markdown Report
    with open(SUMMARY_FILE, 'w') as f:
        f.write("# Integra Market Summary\n\n")
        f.write(summary.to_markdown())
        f.write("\n\n## Top 5 Most Expensive\n")
        top5 = plot_df.sort_values(by='Price', ascending=False).head(5)
        f.write(top5[['Model_Group', 'Title', 'Price', 'Year', 'Mileage_Raw']].to_markdown(index=False))
        
    print(f"Summary saved to {SUMMARY_FILE}")

if __name__ == "__main__":
    main()
