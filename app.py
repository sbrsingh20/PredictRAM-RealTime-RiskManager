import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Define the inflation data as a dictionary
inflation_data = {
    "Sep-22": 6.488240065,
    "Oct-22": 6.084867894,
    "Nov-22": 5.409705648,
    "Dec-22": 5.502392344,
    "Jan-23": 6.155075939,
    "Feb-23": 6.16,
    "Mar-23": 5.793650794,
    "Apr-23": 5.090054816,
    "May-23": 4.418604651,
    "Jun-23": 5.572755418,
    "Jul-23": 7.544264819,
    "Aug-23": 6.912442396,
    "Sep-23": 5.02,
    "Oct-23": 4.87,
    "Nov-23": 5.55,
    "Dec-23": 5.69,
    "Jan-24": 5.1,
    "Feb-24": 5.09,
    "Mar-24": 4.85,
    "Apr-24": 4.83,
    "May-24": 4.75,
    "Jun-24": 5.08,
    "Jul-24": 3.54,
    "Aug-24": 3.65,
    "Sep-24": 5.49
}

# Convert the inflation data to a DataFrame
inflation_df = pd.DataFrame(list(inflation_data.items()), columns=["Date", "Inflation"])
inflation_df["Date"] = pd.to_datetime(inflation_df["Date"], format="%b-%y")
inflation_df.set_index("Date", inplace=True)

# Function to fetch stock data and calculate correlation with inflation
def calculate_stock_inflation_correlation(stock_symbols):
    results = []

    for stock_symbol in stock_symbols:
        # Fetch historical stock data (adjusted close prices)
        stock_data = yf.download(stock_symbol, start="2022-09-01", end="2024-09-30")
        
        # Ensure we have data for stock and inflation for the same period
        merged_data = pd.merge(stock_data['Adj Close'], inflation_df, left_index=True, right_index=True, how="inner")

        # Calculate the correlation
        correlation = merged_data['Adj Close'].corr(merged_data['Inflation'])
        
        # Store the result
        results.append({
            "Stock Symbol": stock_symbol,
            "Correlation with Inflation": correlation
        })

    # Return as a DataFrame
    return pd.DataFrame(results)

# Streamlit Dashboard
def display_dashboard():
    st.title('Stock Inflation Correlation Dashboard')

    # User input for stock symbols
    stock_symbols = st.text_input("Enter Stock Symbols (comma separated):").split(',')

    if len(stock_symbols) > 0:
        stock_symbols = [symbol.strip() for symbol in stock_symbols]
        
        # Calculate the correlation with inflation for the selected stocks
        correlation_df = calculate_stock_inflation_correlation(stock_symbols)

        # Display the results in a table
        st.write("Stock to Inflation Correlation Results", correlation_df)

        # Plot the correlation results
        plt.figure(figsize=(10, 6))
        plt.bar(correlation_df['Stock Symbol'], correlation_df['Correlation with Inflation'], color='skyblue')
        plt.xlabel('Stock Symbol')
        plt.ylabel('Correlation with Inflation')
        plt.title('Correlation of Selected Stocks with Inflation')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
        
        # Display the inflation data along with the stock data
        st.write("Historical Inflation Data", inflation_df)

        # Plot historical inflation data
        plt.figure(figsize=(10, 6))
        plt.plot(inflation_df.index, inflation_df['Inflation'], marker='o', color='orange', label="Inflation Rate")
        plt.xlabel('Date')
        plt.ylabel('Inflation Rate (%)')
        plt.title('Historical Inflation Data')
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

# Run the Streamlit app
if __name__ == "__main__":
    display_dashboard()
