import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuration
st.set_page_config(
    page_title="インテグラの伝説 | 市場分析デモ",
    page_icon="🏎️",
    layout="wide"
)

# Generate Mock Data (Safe for GitHub)
@st.cache_data
def load_data():
    # Creating synthetic data for demonstration purposes
    # This avoids using unauthorized scraped data
    np.random.seed(42)
    n_samples = 100
    
    data = []
    
    # Generate Type R data (Higher price, holds value)
    for _ in range(50):
        year = np.random.randint(1995, 2007)
        mileage = np.random.randint(10000, 160000)
        # Price logic: Base + Year premium - Mileage depreciation
        base_price = 4500000 if year > 2000 else 3500000
        price = base_price - (mileage * 15) + np.random.randint(-200000, 200000)
        price = max(1500000, price) # Minimum floor
        
        data.append({
            "Title": f"ホンダ インテグラ Type R {year}年式",
            "Model_Group": "Integra Type R",
            "Price_Num": price,
            "Year_Num": year,
            "Year_Raw": str(year),
            "Mileage_Num": mileage,
            "Mileage_Raw": f"{mileage/10000:.1f}万km",
            "Region": "Tokyo",
            "URL": "#"
        })
        
    # Generate Standard Integra data (Lower price, normal depreciation)
    for _ in range(50):
        year = np.random.randint(1995, 2007)
        mileage = np.random.randint(20000, 150000)
        base_price = 1500000
        price = base_price - (mileage * 8) + np.random.randint(-100000, 100000)
        price = max(300000, price)
        
        data.append({
            "Title": f"ホンダ インテグラ {year}年式",
            "Model_Group": "Integra",
            "Price_Num": price,
            "Year_Num": year,
            "Year_Raw": str(year),
            "Mileage_Num": mileage,
            "Mileage_Raw": f"{mileage/10000:.1f}万km",
            "Region": "Osaka",
            "URL": "#"
        })
    
    return pd.DataFrame(data)

df = load_data()

# Styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem; 
        font-weight: 800; 
        background: -webkit-linear-gradient(45deg, #e60012, #000); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem; 
        color: #555;
    }
    .highlight {
        color: #e60012; 
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Official Logo or Emoji
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Honda_Logo.svg/320px-Honda_Logo.svg.png", width=100)
    
    st.title("プロジェクト情報")
    
    st.markdown("""
    - **分析者**: Asuka Tsurumoto
    - **データ**: デモ用合成データ
    - **目的**: 市場分析アルゴリズムの展示
    """)
    st.markdown("---")
    st.markdown("[🔗 ポートフォリオに戻る](https://github.com/crane424)")

# --- Section 1: Introduction ---
st.markdown('<p class="main-header">インテグラの伝説 (Demo)</p>', unsafe_allow_html=True)
st.markdown("""
**ホンダ インテグラ Type R** は、JDM黄金時代のアイコンです。
このアプリは、Pythonによるデータ分析と可視化のスキルを示すためのデモアプリケーションです。
※表示されているデータは分析ロジックを示すための**サンプルデータ**です。
""")

# Key Metrics
if not df.empty:
    col1, col2, col3 = st.columns(3)
    type_r_df = df[df['Model_Group'] == 'Integra Type R']
    base_df = df[df['Model_Group'] == 'Integra']

    avg_r = type_r_df['Price_Num'].mean()
    avg_base = base_df['Price_Num'].mean()
    premium_gap = avg_r - avg_base

    col1.metric("Type R 平均価格 (Demo)", f"¥{avg_r/10000:,.1f}万", delta="プレミアム")
    col2.metric("通常モデル 平均価格 (Demo)", f"¥{avg_base/10000:,.1f}万")
    col3.metric("Type Rとの価格差", f"¥{premium_gap/10000:,.1f}万", delta_color="normal")

    st.markdown("---")

    # --- Section 2: The Divide ---
    st.header("1. 大きな分断 (The Great Divide)")
    st.markdown("高性能なType Rと標準モデルの間の価格の乖離を可視化します。")

    fig_scatter = px.scatter(
        df, 
        x="Year_Num", 
        y="Price_Num", 
        color="Model_Group",
        size="Price_Num",
        hover_data=["Title", "Mileage_Raw"],
        color_discrete_map={"Integra Type R": "#e60012", "Integra": "#888888"},
        title="価格 vs 年式 (サンプルデータ)",
        labels={"Price_Num": "価格 (円)", "Year_Num": "年式", "Model_Group": "モデル"}
    )
    fig_scatter.update_layout(yaxis_tickformat=",.0f")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Section 3: The Premium Factors ---
    st.header("2. プレミアムの要因は？")
    st.markdown("走行距離がType Rの価値にどう影響するか（回帰分析デモ）。")

    fig_mileage = px.scatter(
        type_r_df,
        x="Mileage_Num",
        y="Price_Num",
        trendline="ols",
        color="Year_Num",
        hover_data=["Title"],
        title="Type R: 走行距離による価格減価 (サンプル)",
        labels={"Mileage_Num": "走行距離 (km)", "Price_Num": "価格 (円)", "Year_Num": "年式"}
    )
    fig_mileage.update_layout(yaxis_tickformat=",.0f")
    st.plotly_chart(fig_mileage, use_container_width=True)

    # --- Section 4: Market Explorer ---
    st.header("3. データエクスプローラー")
    
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        model_filter = st.multiselect("モデルを選択", options=df['Model_Group'].unique(), default=['Integra Type R'])
    with col_filter2:
        price_threshold = st.slider("上限価格 (万円)", 0, int(df['Price_Num'].max()/10000), 500)

    filtered_df = df[
        (df['Model_Group'].isin(model_filter)) & 
        (df['Price_Num'] <= price_threshold * 10000)
    ]

    st.dataframe(
        filtered_df[['Title', 'Model_Group', 'Price_Num', 'Year_Raw', 'Mileage_Raw', 'Region']],
        column_config={
            "Price_Num": st.column_config.NumberColumn("価格 (円)", format="¥%d"),
            "Title": "タイトル",
            "Model_Group": "モデル",
            "Year_Raw": "年式",
            "Mileage_Raw": "走行距離",
            "Region": "地域"
        },
        hide_index=True
    )
    
st.markdown("---")
st.markdown("Created with ❤️ by Asuka Tsurumoto")
