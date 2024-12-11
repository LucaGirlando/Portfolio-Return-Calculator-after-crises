# Portfolio-Return-Calculator-after-crises
A Streamlit app to calculate portfolio returns during historical economic crises. Users can allocate assets, select specific periods, and assess events like the 2008 Financial Crisis or the COVID-19 Pandemic. It integrates Yahoo Finance data, offering insights on asset performance under varying market conditions

## Overview:
The Portfolio Return Calculator is an interactive web application designed to help users calculate the return of a portfolio or individual assets based on historical events that had major economic impacts over the last two decades. The app allows users to choose asset allocations, select specific time horizons based on different historical crises, and visualize how portfolios performed during these events.
The app leverages financial data from Yahoo Finance and displays detailed performance insights for a range of assets, including equity indices, bonds, and commodities. It provides an easy-to-understand platform to explore historical performance and simulate portfolio returns before key crises in modern history.

## Key Features:
Portfolio Allocation: Choose from a selection of asset classes, including major stock indices (S&P 500, MSCI World, etc.), bonds, and commodities.
Historical Crisis Analysis: Calculate portfolio returns based on the start of key economic crises such as the 2008 financial crisis, the 2010 European sovereign debt crisis, Brexit in 2016, the 2020 COVID-19 pandemic, and the 2022 Russia-Ukraine war.
Customizable Allocations: Adjust portfolio weights to suit specific investment strategies and calculate returns accordingly.
Time Horizon Selection: Analyze portfolio performance based on data from different start dates, aligned with historical crises, to see how each asset performed during each event.
Performance Data: Visualize and explore asset performance during crises with interactive charts.
Return Calculations: Get average annual returns based on historical data from Yahoo Finance and calculate the impact of asset allocations during crises.

## Usage:
Set Up Your Portfolio: Choose the assets you want to include in your portfolio and allocate a percentage to each asset. The sum of all allocations must equal 100%.
Choose a Crisis Event: Select a start date corresponding to a major economic crisis. This determines the time period over which performance is analyzed.
View Historical Performance: View a detailed analysis of asset returns, including performance metrics during crises and visual charts.
Download Results: For a more in-depth review, download the performance data and crisis details in a user-friendly format.

## Requirements:
Python 3.x: The application is built in Python and requires version 3 or higher.
Streamlit: To run the web app interface. Install via pip install streamlit.
Pandas: For data handling and processing. Install via pip install pandas.
NumPy: Required for numerical calculations. Install via pip install numpy.
yFinance: For fetching historical financial data from Yahoo Finance. Install via pip install yfinance.
Matplotlib: For basic charting functionality. Install via pip install matplotlib.
Plotly: For interactive graphs and visualizations. Install via pip install plotly.
