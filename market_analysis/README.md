# 🏎️ The Legend of Integra: Market Analysis

An automated data storytelling project that investigates the price premium of the Honda Integra Type R in the current used car market.

![Price Trends](price_trends.png)

## 📖 The Story
The Honda Integra Type R (DC2/DC5) is a JDM icon. But as prices soar for 90s sports cars, how much of a premium does the "Red Badge" really command? 

This project scrapes real-time data from major Japanese used car listings to visualize:
1. **The Gap**: The stark price difference between base models and the Type R.
2. **The Drivers**: How mileage and model year correlate with collector value.
3. **The Market**: A tool for potential buyers to hunt for deals.

## 🛠️ Tech Stack
- **Python**: Core logic and scraping.
- **Streamlit**: Interactive web dashboard.
- **Plotly**: Data visualization.
- **BeautifulSoup**: HTML parsing.
- **Pandas**: Data manipulation.

## 🚀 How to Run

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd market_analysis
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the App**
```bash
streamlit run app.py
```

4. **(Optional) Update Data**
   Run the scraper to fetch fresh data:
```bash
python scraper.py
```

## 📊 Key Findings
- The **Type R Premium** is real: On average, Type R models trade at **double** the price of standard models.
- **Low Mileage is King**: Collectors' examples (<50k km) show exponential price increases, decoupling from standard depreciation curves.

## 👨‍💻 Author
**Asuka Tsurumoto**  
[Portfolio](file:///Users/shiroashi3/Desktop/my_homepage/index.html)
