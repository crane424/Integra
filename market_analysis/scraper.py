import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Configurations
BASE_URLS = [
    {"url": "https://www.carsensor.net/usedcar/bHO/s008/index.html", "model": "Integra"},
    {"url": "https://www.carsensor.net/usedcar/bHO/s010/index.html", "model": "Integra Type R"}
]
OUTPUT_FILE = "market_analysis/integra_market_data.csv"

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_listings(soup, model_name):
    listings = []
    # The main container for each car listing
    cars = soup.select('.cassetteMain')
    
    for car in cars:
        try:
            # Title
            title_elem = car.select_one('.cassetteMain__title')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            # Link
            link_elem = car.select_one('.cassetteMain__link')
            link = link_elem['href'] if link_elem else ""
            if link and not link.startswith('http'):
                link = "https://www.carsensor.net" + link

            # Prices
            # Total Price matches class 'totalPrice__content' (usually contains numbers + 万円)
            total_price_elem = car.select_one('.totalPrice__content')
            total_price_text = total_price_elem.get_text(strip=True) if total_price_elem else ""

            # Base Price
            base_price_elem = car.select_one('.basePrice__content')
            base_price_text = base_price_elem.get_text(strip=True) if base_price_elem else ""

            # Specs (Year, Mileage) are often in a definition list dl/dt/dd or table
            # Based on inspection, looking for specific text in dt
            year = "Unknown"
            mileage = "Unknown"
            
            dts = car.select('dt')
            for dt in dts:
                dt_text = dt.get_text(strip=True)
                if "年式" in dt_text:
                    dd = dt.find_next_sibling('dd')
                    if dd: year = dd.get_text(strip=True)
                elif "走行" in dt_text:
                    dd = dt.find_next_sibling('dd')
                    if dd: mileage = dd.get_text(strip=True)

            # Region
            # Usually in .cassetteSub__area p or similar
            # Implementation: look for the shop info area
            region = "Unknown"
            # Attempt to find region in shop area
            shop_area = car.select_one('.cassetteMain__shop')
            if shop_area:
                # Sometimes it's the first p tag, or specific class
                p_tags = shop_area.find_all('p')
                for p in p_tags:
                    # Simple heuristic: regions often don't have numbers or '車台番号'
                    # But checking if it matches known prefectures might be overkill.
                    # Let's just grab the text of the paragraph that likely contains it.
                    # Often the region is short.
                    text = p.get_text(strip=True)
                    if text and len(text) < 10: 
                        region = text
                        break

            listings.append({
                "Model_Group": model_name,
                "Title": title,
                "Total_Price_Raw": total_price_text,
                "Base_Price_Raw": base_price_text,
                "Year_Raw": year,
                "Mileage_Raw": mileage,
                "Region": region,
                "URL": link
            })
            
        except Exception as e:
            print(f"Error parsing a car: {e}")
            continue
            
    return listings

def main():
    all_data = []

    for source in BASE_URLS:
        url = source["url"]
        model = source["model"]
        print(f"Scraping {model} starting at {url}...")
        
        while url:
            soup = get_soup(url)
            if not soup:
                break
            
            data = extract_listings(soup, model)
            print(f"  Found {len(data)} listings on this page.")
            all_data.extend(data)
            
            # Pagination: Find 'Next' button
            # Class usually .pager__next or similar link text '次へ' or '>'
            next_link = soup.select_one('.pager__next a')
            if next_link:
                href = next_link.get('href')
                if href:
                    if not href.startswith('http'):
                        url = "https://www.carsensor.net" + href
                    else:
                        url = href
                    time.sleep(1) # Be polite
                else:
                    url = None
            else:
                # Check for other pagination types if .pager__next missing
                # Sometimes it's a list item with class 'next'
                next_li = soup.select_one('li.next a')
                if next_li:
                     href = next_li.get('href')
                     url = "https://www.carsensor.net" + href
                     time.sleep(1)
                else:
                    url = None
        
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Scraping complete. Saved {len(df)} listings to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
