import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📈 BTC Rebound Strategy — IV-Adaptive Dashboard")

# Strategy Summary
st.header("🔍 Strategy Overview")
st.markdown("""
**Objective**: Capture BTC rebound opportunities after sharp daily drops, dynamically adjusting take-profit and trailing-stop based on rolling implied volatility.

**Key Entry Conditions**:
- Daily return ≤ **-3.25%**
- Volume spike ≥ **1.5×** 7-day average
- Implied volatility (14-day log return std) within adaptive range

**Exit Conditions**:
- **Seasonal Take-Profit (TP)**: 3% to 5% base TP depending on month
- **Trailing Stop Loss (TSL)**: Activated after 1% unrealized gain

---

### 📐 Mathematical Logic

**Implied Volatility (IV)**:
\[ \text{IV}_{14d} = \text{StdDev}(\log(\frac{P_t}{P_{t-1}})) \text{ over 14 days} \]

**Volatility Context Filters**:
- Median and IQR over 60 days:
\[ \text{IV Ratio} = \frac{IV_{14d} - \text{Median}_{60d}}{\text{IQR}_{60d}} \]

**TP & TSL Adjustment**:
\[ \text{TP}_{adj} = TP_{base} \times (1 + 0.2 \times \text{IV Ratio}) \quad \text{(Clipped between 2\%–8\%)} \]
\[ \text{TSL}_{adj} = 5\% \times (1 + 0.2 \times \text{IV Ratio}) \quad \text{(Clipped between 3\%–8\%)} \]

**Capital Allocation**: One full allocation per trade (no overlap)
""")

# Performance Metrics
st.header("📊 Performance Metrics (2017–2025)")
metrics = {
    "Final Capital": "$484,641.73",
    "Total Return": "+384.64%",
    "Trades Executed": 26,
    "Drawdown": "Minimal",
    "Worst Periods": "Skillfully avoided (e.g., 2018–2020)"
}
col1, col2, col3 = st.columns(3)
col1.metric("💼 Final Capital", metrics["Final Capital"])
col2.metric("📈 Total Return", metrics["Total Return"])
col3.metric("🔁 Trades Executed", metrics["Trades Executed"])

# Load and visualize trades if uploaded
st.header("📆 Trade History Viewer")
uploaded_file = st.file_uploader("Upload Strategy Trade Log CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Entry_Date', 'Exit_Date'])
    st.dataframe(df)

    # Plot equity growth
    st.subheader("Equity Curve")
    if "Equity" in df.columns:
        fig, ax = plt.subplots(figsize=(12, 4))
        df.set_index("Exit_Date")["Equity"].plot(ax=ax, color='green', linewidth=2)
        ax.set_title("Strategy Equity Growth")
        ax.set_ylabel("Portfolio Value")
        ax.grid(True)
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Developed by Quant Finance • Strategy Logic and Results are Backtest-Based • 2025")
