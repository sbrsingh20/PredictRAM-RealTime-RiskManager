import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import time

# Function to fetch stock data for multiple stocks
def fetch_stock_data(stock_symbols, start_date="2022-01-01", end_date="2024-01-01"):
    # Append .NS to Indian stock symbols
    stock_symbols_ns = [symbol + ".NS" for symbol in stock_symbols]
    
    # Download stock data from Yahoo Finance
    stock_data = yf.download(stock_symbols_ns, start=start_date, end=end_date)['Adj Close']
    return stock_data

# Function to calculate Portfolio Return on Investment (ROI)
def calculate_roi(stock_data):
    initial_value = stock_data.iloc[0]  # Price at the start of the period
    final_value = stock_data.iloc[-1]  # Price at the end of the period
    portfolio_roi = (final_value.sum() - initial_value.sum()) / initial_value.sum()
    return portfolio_roi

# Function to calculate Portfolio Sharpe Ratio
def calculate_sharpe_ratio(stock_data, risk_free_rate=0.05):
    # Calculate daily returns
    daily_returns = stock_data.pct_change().mean(axis=1)
    
    # Calculate excess returns over the risk-free rate
    excess_returns = daily_returns - (risk_free_rate / 252)  # Annualized risk-free rate divided by 252 trading days
    
    # Calculate the standard deviation (volatility) of excess returns
    volatility = daily_returns.std() * np.sqrt(252)  # Annualized standard deviation
    
    # Sharpe ratio: excess returns / volatility
    sharpe_ratio = excess_returns.mean() / volatility
    return sharpe_ratio

# Function to calculate Sortino Ratio
def calculate_sortino_ratio(stock_data, risk_free_rate=0.05):
    # Calculate daily returns
    daily_returns = stock_data.pct_change().mean(axis=1)
    
    # Calculate downside deviation (only negative returns are considered)
    negative_returns = daily_returns[daily_returns < 0]
    downside_deviation = negative_returns.std() * np.sqrt(252)
    
    # Calculate excess returns over the risk-free rate
    excess_returns = daily_returns - (risk_free_rate / 252)
    
    # Sortino ratio: excess returns / downside deviation
    sortino_ratio = excess_returns.mean() / downside_deviation
    return sortino_ratio

# Function to calculate Treynor Ratio
def calculate_treynor_ratio(stock_data, market_data, risk_free_rate=0.05):
    # Calculate daily returns for the portfolio
    portfolio_returns = stock_data.pct_change().mean(axis=1)
    
    # Calculate beta of the portfolio with respect to the market (using covariance and variance)
    covariance = np.cov(portfolio_returns, market_data.pct_change())[0][1]
    market_variance = np.var(market_data.pct_change())
    beta = covariance / market_variance
    
    # Calculate excess returns
    excess_returns = portfolio_returns.mean() - (risk_free_rate / 252)
    
    # Treynor ratio: excess return / beta
    treynor_ratio = excess_returns / beta
    return treynor_ratio

# Function to calculate Information Ratio
def calculate_information_ratio(stock_data, benchmark_data):
    # Calculate daily returns for the portfolio and benchmark
    portfolio_returns = stock_data.pct_change().mean(axis=1)
    benchmark_returns = benchmark_data.pct_change()
    
    # Calculate tracking error (standard deviation of excess returns)
    excess_returns = portfolio_returns - benchmark_returns
    tracking_error = excess_returns.std() * np.sqrt(252)
    
    # Information ratio: excess return / tracking error
    information_ratio = excess_returns.mean() / tracking_error
    return information_ratio

# Function to calculate Portfolio Turnover
def calculate_portfolio_turnover(stock_data):
    # Calculate daily returns and identify changes in portfolio allocations
    daily_returns = stock_data.pct_change().abs()
    
    # Turnover is the sum of absolute changes in allocation
    turnover = daily_returns.sum() / len(stock_data)
    return turnover

# Function to load and display data from Excel
def load_excel_data(excel_file):
    # Load Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file)
    return df

# Main function to calculate and display the portfolio performance
def display_portfolio_performance():
    st.title('Real-Time Portfolio Performance and Stock Correlations Dashboard')

    # Get stock symbols as input
    stock_symbols = st.multiselect("Select Stock Symbols", ["TCS", "INFY", "RELIANCE", "HDFC", "BAJFINANCE", "ICICIBANK"])

    # Load the existing Excel information
    excel_file = "India Inflation CPI Consumer Price Index_event_stock_analysis_resultsOct.xlsx"
    df_excel = load_excel_data(excel_file)
    st.subheader("Stock Correlations from Excel Data")
    st.dataframe(df_excel)

    # Create an empty placeholder for real-time updates
    performance_placeholder = st.empty()
    
    # Loop for real-time updates every 30 seconds
    while True:
        if len(stock_symbols) > 0:
            # Fetch stock data
            stock_data = fetch_stock_data(stock_symbols)

            # Display Portfolio ROI
            portfolio_roi = calculate_roi(stock_data)
            sharpe_ratio = calculate_sharpe_ratio(stock_data)
            sortino_ratio = calculate_sortino_ratio(stock_data)

            # Fetch market data for Treynor and Information ratios (use Nifty index as a proxy)
            market_data = yf.download("^NSEI", start="2022-01-01", end="2024-01-01")['Adj Close']
            
            treynor_ratio = calculate_treynor_ratio(stock_data, market_data)
            benchmark_data = yf.download("^NSEI", start="2022-01-01", end="2024-01-01")['Adj Close']
            information_ratio = calculate_information_ratio(stock_data, benchmark_data)
            turnover = calculate_portfolio_turnover(stock_data)

            # Clear and update the performance placeholder dynamically
            with performance_placeholder:
                st.subheader("Real-Time Portfolio Performance Metrics")
                st.write(f"Portfolio ROI: {portfolio_roi:.2%}")
                st.write(f"Sharpe Ratio: {sharpe_ratio:.2f}")
                st.write(f"Sortino Ratio: {sortino_ratio:.2f}")
                st.write(f"Treynor Ratio: {treynor_ratio:.2f}")
                st.write(f"Information Ratio: {information_ratio:.2f}")
                st.write(f"Portfolio Turnover: {turnover:.2%}")
        
        # Wait for 30 seconds before refreshing data
        time.sleep(30)

# Run the app
if __name__ == "__main__":
    display_portfolio_performance()
