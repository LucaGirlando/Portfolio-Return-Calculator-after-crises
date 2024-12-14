import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import sys
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.markdown("""
    <p style="font-size: 12px; text-align: center;">
        Created by: <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a>
    </p>
""", unsafe_allow_html=True)
# Title of the app
st.title("Portfolio Return Calculator")

st.header("Before the historical crises")

# Description under the title
st.markdown("""
This program is designed to analyze and showcase the performance of a portfolio (or a single asset) as if it were purchased shortly before the most significant economic crises of the past 20 years. By simulating investment returns during turbulent market periods, it offers valuable insights into the resilience and recovery of various assets or portfolios. Whether you're looking to understand how a portfolio might have fared in challenging economic conditions or aiming to assess long-term investment strategies, this tool provides a comprehensive analysis to help inform your financial decisions.
""")

# Section to choose asset allocation
st.header("Choose your portfolio allocation")

# Available assets (ETFs with corresponding index tickers as fallback)
assets = {

    "S&P 500 Index": ("SPY", "^GSPC"),  # S&P 500 ETF, S&P 500 index
    "MSCI World": ("IWDA.L", "^WORLD"),  # MSCI World ETF, MSCI World index
    "Stoxx 600 Index": ("EXSA.DE", "^STOXX50E"),  # Stoxx 600 ETF, Stoxx 600 index
    "Russell 2000 Index": ("IWM", "^RUT"),  # Russell 2000 ETF, Russell 2000 index
    "MSCI Emerging Markets Index": ("EEM", "^MSCIEM"),  # MSCI Emerging Markets ETF, MSCI Emerging Markets index
    "Nikkei 225 Index": ("EWJ", "^N225"),  # Nikkei 225 ETF, Nikkei 225 index
    "Global Government Bonds": ("BWX", "^IRX"),  # Global Government Bonds ETF, T-Bill index
    "European Bonds": ("IBGL.L", "^IRXEU"),  # European Bonds ETF, European Government Bonds index
    "Gold": ("GLD", "^XAUUSD=X")  # Gold ETF, Gold index (XAU/USD)
}

# Asset sliders
allocations = {}
total_allocation = 0
for asset in assets:
    allocations[asset] = st.slider(f"{asset} (%)", min_value=0, max_value=100, value=0, step=1)
    total_allocation += allocations[asset]

# Check if total allocation is 100%
if total_allocation != 100:
    st.warning(f"The total allocation must be 100%. Currently, it's {total_allocation}%.")
    st.stop()

# Section to choose the time horizon based on historical events
st.header("Choose the time horizon (based on historical events)")

# Historical events
specific_dates = {
    "Since January 2008 (Financial Crisis)": "2008-01-01",
    "Since January 2010 (European Sovereign Debt Crisis)": "2010-01-01",
    "Since January 2016 (Pre-Brexit)": "2016-01-01",
    "Since January 2020 (Pre-COVID Pandemic)": "2020-01-01",
    "Since January 2022 (Pre-Russia-Ukraine War)": "2022-01-01"
}

specific_start_date = st.selectbox("Choose a specific start date", options=list(specific_dates.keys()))

# Display information about the chosen crisis
def display_crisis_info(start_date):
    crisis_info = {
        "2008-01-01": {
            "title": "2008 Financial Crisis",
            "description": "The 2008 Financial Crisis was a global financial meltdown triggered by the collapse of Lehman Brothers and a sharp decline in housing prices in the U.S. It led to widespread financial losses, stock market crashes, and a global recession.",
            "global_impact": {
                "S&P 500": -57.69,  # Peak-to-trough drop during the crisis
                "Nikkei 225": -60.12,  # Peak-to-trough drop during the crisis
                "FTSE 100": -49.50,  # Peak-to-trough drop during the crisis
                "MSCI Emerging Markets": -58.10,  # Peak-to-trough drop during the crisis
                "Gold": +25.98,  # Peak-to-trough performance
                "DAX 30": -55.00,  # Peak-to-trough drop during the crisis
                "MSCI World": -54.00,  # Peak-to-trough drop during the crisis
                "Hang Seng": -53.50,  # Peak-to-trough drop during the crisis
                "FTSE MIB": -55.75,  # Peak-to-trough drop during the crisis
                "US Treasuries (10Y)": +12.00,  # Price increase during crisis
                "German Bunds (10Y)": +7.50,  # Price increase during crisis
                
            }
        },
        "2010-01-01": {
            "title": "2010 European Sovereign Debt Crisis",
            "description": "The European Sovereign Debt Crisis occurred when several European countries, particularly Greece, faced high government debt and were unable to repay or refinance their debts. This caused instability in European financial markets.",
            "global_impact": {
                "S&P 500": -16.99,  # Peak-to-trough drop during the crisis
                "Nikkei 225": -19.95,  # Peak-to-trough drop during the crisis
                "FTSE 100": -17.71,  # Peak-to-trough drop during the crisis
                "MSCI Emerging Markets": -23.56,  # Peak-to-trough drop during the crisis
                "Gold": +11.25,  # Peak-to-trough performance
                "DAX 30": -17.50,  # Peak-to-trough drop during the crisis
                "MSCI World": -15.00,  # Peak-to-trough drop during the crisis
                "Hang Seng": -18.00,  # Peak-to-trough drop during the crisis
                "FTSE MIB": -20.00,  # Peak-to-trough drop during the crisis
                "US Treasuries (10Y)": +5.80,  # Price increase during crisis
                "German Bunds (10Y)": +3.50,  # Price increase during crisis
                
            }
        },
        "2016-01-01": {
            "title": "2016 Brexit Vote",
            "description": "The Brexit vote in June 2016 led to the UK's decision to leave the European Union, causing significant uncertainty and volatility in financial markets, particularly in the UK and Europe.",
            "global_impact": {
                "S&P 500": -5.34,  # Peak-to-trough drop during the crisis
                "Nikkei 225": -20.02,  # Peak-to-trough drop during the crisis
                "FTSE 100": -12.00,  # Peak-to-trough drop during the crisis
                "MSCI Emerging Markets": -16.76,  # Peak-to-trough drop during the crisis
                "Gold": +8.45,  # Peak-to-trough performance
                "DAX 30": -8.50,  # Peak-to-trough drop during the crisis
                "MSCI World": -7.00,  # Peak-to-trough drop during the crisis
                "Hang Seng": -10.00,  # Peak-to-trough drop during the crisis
                "FTSE MIB": -9.50,  # Peak-to-trough drop during the crisis
                "US Treasuries (10Y)": +3.50,  # Price increase during crisis
                "German Bunds (10Y)": +2.00,  # Price increase during crisis
                "BTPs (10Y)": +2.80  # Price increase during crisis
            }
        },
        "2020-01-01": {
            "title": "2020 COVID-19 Pandemic",
            "description": "The COVID-19 pandemic caused widespread global health crises, followed by massive economic downturns. The pandemic led to lockdowns, business closures, and market turmoil.",
            "global_impact": {
                "S&P 500": -33.92,  # Peak-to-trough drop during the crisis
                "Nikkei 225": -31.86,  # Peak-to-trough drop during the crisis
                "FTSE 100": -32.84,  # Peak-to-trough drop during the crisis
                "MSCI Emerging Markets": -34.80,  # Peak-to-trough drop during the crisis
                "Gold": +42.93,  # Peak-to-trough performance
                "DAX 30": -39.00,  # Peak-to-trough drop during the crisis
                "MSCI World": -38.50,  # Peak-to-trough drop during the crisis
                "Hang Seng": -30.00,  # Peak-to-trough drop during the crisis
                "FTSE MIB": -35.00,  # Peak-to-trough drop during the crisis
                "US Treasuries (10Y)": +5.20,  # Price increase during crisis
                "German Bunds (10Y)": +3.80,  # Price increase during crisis
                "BTPs (10Y)": +4.50  # Price increase during crisis
            }
        },
        "2022-01-01": {
            "title": "2022 Russia-Ukraine War",
            "description": "The Russia-Ukraine war, which began in February 2022, caused severe geopolitical instability, energy price shocks, and a major crisis in global supply chains.",
            "global_impact": {
                "S&P 500": -23.22,  # Peak-to-trough drop during the crisis
                "Nikkei 225": -16.52,  # Peak-to-trough drop during the crisis
                "FTSE 100": -17.68,  # Peak-to-trough drop during the crisis
                "MSCI Emerging Markets": -21.15,  # Peak-to-trough drop during the crisis
                "Gold": +6.94,  # Peak-to-trough performance
                "DAX 30": -20.00,  # Peak-to-trough drop during the crisis
                "MSCI World": -19.50,  # Peak-to-trough drop during the crisis
                "Hang Seng": -18.00,  # Peak-to-trough drop during the crisis
                "FTSE MIB": -22.00,  # Peak-to-trough drop during the crisis
                "US Treasuries (10Y)": +2.50,  # Price increase during crisis
                "German Bunds (10Y)": +1.90,  # Price increase during crisis
                "BTPs (10Y)": +3.00  # Price increase during crisis
            }
        }
    }

    crisis = crisis_info.get(start_date, {})
    if crisis:
        st.subheader(crisis["title"])
        st.write(crisis["description"])
        st.write("Performance of some global indices during the crisis:")
        crisis_df = pd.DataFrame(list(crisis["global_impact"].items()), columns=["Asset", "Peak-to-Trough Loss (%)"])
        st.dataframe(crisis_df)

# Show information about the selected crisis
if specific_start_date:
    start_date = specific_dates[specific_start_date]
    display_crisis_info(start_date)

# Function to get average annual return using yfinance
def get_average_annual_return(ticker, start_date):
    try:
        data = yf.download(ticker, start=start_date, interval="1mo")
        if data.empty:
            st.warning(f"No data available for {ticker}.")
            return None  # Return None if data is unavailable
        data = data["Adj Close"].dropna()
        returns = data.pct_change().dropna()
        avg_return = (1 + returns.mean()) ** 12 - 1  # Annualized return
        return avg_return.item() if hasattr(avg_return, 'item') else avg_return
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Don't calculate or show returns until a start date is selected
if specific_start_date:
    # Calculate the average annual returns
    returns_data = {}
    start_date = specific_dates[specific_start_date]  # Chosen start date

    # Extract the start year from the specific start date
    start_year = int(start_date.split('-')[0])  # Extract only the year

    for asset, (etf_ticker, index_ticker) in assets.items():
        # Only calculate returns for assets that have been selected (allocation > 0)
        if allocations[asset] > 0:
            # Try first with the ETF
            etf_data = get_average_annual_return(etf_ticker, start_date)

            # If ETF data is unavailable, try the index
            if etf_data is None:
                st.warning(f"No data available for {asset} ({etf_ticker}), using data from the index {index_ticker}.")
                etf_data = get_average_annual_return(index_ticker, start_date)

            returns_data[asset] = etf_data

    # Calculate the total portfolio return
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Portfolio Return</h1>", unsafe_allow_html=True)

    portfolio_return = sum(
       allocations[asset] / 100 * ((1 + returns_data[asset]) ** (datetime.today().year - start_year) - 1)
       for asset in returns_data
    )

    # Calculate annualized return
    num_years = datetime.today().year - start_year
    annualized_return = (1 + portfolio_return) ** (1 / num_years) - 1

    # Calculate future portfolio values for given investments
    investment_10k = 10000 * (1 + portfolio_return)
    investment_100k = 100000 * (1 + portfolio_return)

    # Highlight the result in a visually appealing way
    st.markdown(f"""
    <div style="font-size: 24px; font-weight: bold; text-align: center; color: #FF5722;">
        The total return of your portfolio based on the chosen time horizon is: 
        <span style="font-size: 32px; color: #4CAF50;">{portfolio_return * 100:.2f}%</span>
    </div>
    <div style="font-size: 20px; text-align: center; color: white; margin-top: 20px;">
        The annualized return is: <span style="font-size: 28px; color: #4CAF50;">{annualized_return * 100:.2f}%</span>.
        <br><br>
        If you had invested <strong>$10,000</strong>, your portfolio would now be worth: 
        <span style="font-size: 28px; color: #4CAF50;">${investment_10k:,.2f}</span>.
        <br>
        If you had invested <strong>$100,000</strong>, your portfolio would now be worth: 
        <span style="font-size: 28px; color: #4CAF50;">${investment_100k:,.2f}</span>.
    </div>
    """, unsafe_allow_html=True)

    # Create the table of individual asset returns (sorted)
    st.header("Individual Asset Returns")
    asset_returns = [(asset, (1 + returns_data[asset]) ** (datetime.today().year - start_year) - 1) for asset in returns_data]
    asset_returns_sorted = sorted(asset_returns, key=lambda x: x[1], reverse=True)

    # Display the table
    df_returns = pd.DataFrame(asset_returns_sorted, columns=["Asset", "Compound Return (%)"])
    df_returns["Compound Return (%)"] = df_returns["Compound Return (%)"] * 100  # Convert to percentage
    st.dataframe(df_returns)

    # Plot the individual asset returns over time
    st.header("Individual Asset Return Graph")

# Initialize an empty DataFrame for plotting data
plot_data = pd.DataFrame()

# Fetch and process historical data for each asset
for asset, (etf_ticker, index_ticker) in assets.items():
    if allocations[asset] > 0:  # Include only user-selected assets
        # Determine the appropriate ticker (ETF or fallback index)
        ticker = etf_ticker if returns_data.get(asset) is not None else index_ticker

        try:
            # Fetch historical data and calculate cumulative returns
            data = yf.download(ticker, start=start_date, interval="1mo")["Adj Close"]
            data = data.pct_change().cumsum()  # Calculate cumulative percentage returns
            plot_data[asset] = data  # Add to the plot DataFrame
        except Exception as e:
            st.warning(f"Unable to retrieve data for {asset} ({ticker}): {e}")

# Create the plot using Plotly
if not plot_data.empty:
    fig = go.Figure()

    # Add a line for each asset
    for asset in plot_data.columns:
        fig.add_trace(go.Scatter(
            x=plot_data.index,
            y=plot_data[asset],
            mode='lines',
            name=asset  # Name appears in the legend
        ))

    # Customize layout for better readability
    fig.update_layout(
        title="Cumulative Returns Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Returns (%)",
        legend_title="Assets",
        template="plotly_white",
        height=400,  # Lower height for a shorter graph
        width=1000,  # Increase width for a longer graph
        margin=dict(l=40, r=40, t=40, b=40)  # Add spacing for a clean layout
    )

    # Show the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No data available to plot. Please check your asset selection and start date.")
