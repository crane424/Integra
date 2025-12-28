# Honda Integra Market Analysis

## 🏎️ Project Overview
This project analyzes the used car market trends for the **Honda Integra**, specifically comparing the price appreciation and market behavior of the high-performance **Type R** models versus standard grades.

**Live App**: [https://integra-analysis.streamlit.app/](https://integra-analysis.streamlit.app/)

## 📈 Insights
-   **Price Gap**: Identified a significant price premium for Type R models (Mean: ¥2.64M) compared to standard models (Mean: ¥1.23M).
-   **Trend Analysis**: Visualized price distribution and correlation with mileage/year using synthetic market data (for demonstration).

## 🛠️ Technology Stack
-   **Python 3.9+**
-   **Data Processing**: `pandas`, `numpy`
-   **Visualization**: `matplotlib`
-   **App Framework**: `streamlit`

## 📂 Project Structure
```text
├── Integra/
│   ├── app.py          # Main Streamlit application
│   ├── data.csv        # Market data (synthetic or scraped)
│   ├── requirements.txt
│   └── ...
```

## 🚀 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/Integra_Analysis.git
    cd Integra_Analysis
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app**
    ```bash
    streamlit run app.py
    ```
