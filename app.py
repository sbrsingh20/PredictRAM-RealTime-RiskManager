import pandas as pd
import streamlit as st
import yfinance as yf

# File path for the stock data (ensure the file exists in the root directory)
file_path = 'merged_stock_data_with_categories_in_cells_nov2024.xlsx'

# Define the categorization function and helper methods (same as before)
def categorize_risk(value, thresholds):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "Data not available"

    if value < thresholds[0]:
        return "Good"
    elif thresholds[0] <= value <= thresholds[1]:
        return "Neutral"
    else:
        return "Bad"

def get_parameter_description(param, risk_level):
    descriptions = {
        "Volatility": {
            "Good": "Volatility is low, indicating less risk.",
            "Neutral": "Volatility is moderate.",
            "Bad": "Volatility is high, indicating more risk."
        },
        "Beta": {
            "Good": "Beta is low, less sensitive to market movements.",
            "Neutral": "Beta is moderate.",
            "Bad": "Beta is high, indicating higher risk relative to the market."
        },
        "Profit Margins": {
            "Good": "Profit margins are strong, indicating good financial health.",
            "Neutral": "Profit margins are average.",
            "Bad": "Profit margins are low, indicating potential financial issues."
        },
        "currentRatio": {
            "Good": "Current ratio is strong, indicating good liquidity.",
            "Neutral": "Current ratio is adequate.",
            "Bad": "Current ratio is low, indicating liquidity issues."
        },
    }
    return descriptions.get(param, {}).get(risk_level, "No description available.")

def get_risk_color(risk_level):
    if risk_level == "Good":
        return "green"
    elif risk_level == "Neutral":
        return "yellow"
    elif risk_level == "Bad":
        return "red"
    else:
        return "black"

# Create a function to fetch inflation data and calculate the correlation
def calculate_inflation_correlation(stock_symbols, inflation_data, start_date, end_date):
    """Calculates the correlation of stock returns with inflation."""
    # Convert the inflation data into a pandas DataFrame
    inflation_df = pd.DataFrame(inflation_data, columns=["Date", "Inflation Rate"])
    inflation_df['Date'] = pd.to_datetime(inflation_df['Date'])
    inflation_df.set_index('Date', inplace=True)

    # Fetch stock data using yfinance
    stock_data = {}
    for symbol in stock_symbols:
        stock_data[symbol] = yf.download(symbol, start=start_date, end=end_date)['Adj Close']

    # Calculate returns for each stock
    returns = {symbol: stock_data[symbol].pct_change().dropna() for symbol in stock_symbols}

    # Merge stock returns with inflation data (using intersection of dates)
    inflation_resampled = inflation_df.resample('D').ffill()  # Resample inflation data to daily frequency
    correlation_results = {}

    for symbol, stock_returns in returns.items():
        merged_data = pd.concat([stock_returns, inflation_resampled], axis=1, join='inner')
        merged_data.columns = ['Stock Return', 'Inflation Rate']
        correlation = merged_data.corr().iloc[0, 1]  # Get the correlation between stock return and inflation rate
        correlation_results[symbol] = correlation

    return correlation_results

def display_dashboard():
    st.title('Stock Risk Dashboard')

    # Read the stock data from the pre-defined Excel file
    df = pd.read_excel(file_path)

    # Get stock symbols input from the user
    stock_symbols = st.multiselect("Select Stock Symbols", df['Stock Symbol'].unique())
    
    if len(stock_symbols) > 0:
        # Define the start and end dates based on available inflation data
        start_date = '2022-09-01'
        end_date = '2024-09-30'

        # Define inflation data
        inflation_data = [
            ('2022-09-01', 6.488240065), ('2022-10-01', 6.084867894), ('2022-11-01', 5.409705648),
            ('2022-12-01', 5.502392344), ('2023-01-01', 6.155075939), ('2023-02-01', 6.16),
            ('2023-03-01', 5.793650794), ('2023-04-01', 5.090054816), ('2023-05-01', 4.418604651),
            ('2023-06-01', 5.572755418), ('2023-07-01', 7.544264819), ('2023-08-01', 6.912442396),
            ('2023-09-01', 5.02), ('2023-10-01', 4.87), ('2023-11-01', 5.55), ('2023-12-01', 5.69),
            ('2024-01-01', 5.1), ('2024-02-01', 5.09), ('2024-03-01', 4.85), ('2024-04-01', 4.83),
            ('2024-05-01', 4.75), ('2024-06-01', 5.08), ('2024-07-01', 3.54), ('2024-08-01', 3.65),
            ('2024-09-01', 5.49)
        ]

        # Calculate the correlation with inflation
        correlation_results = calculate_inflation_correlation(stock_symbols, inflation_data, start_date, end_date)

        # Display the results
        st.write("Stock Correlation with Inflation", correlation_results)

        # Display risk data (same as before)
        risk_categories = {
            # Same risk categories and thresholds as before
        }
        risk_data = calculate_risk_parameters(stock_symbols, file_path, risk_categories)
        st.write("Stock Risk Data", risk_data)

        # You can add more visualizations (e.g., pie chart, bar chart, etc.) if needed
        risk_counts = risk_data.groupby("Risk Level").size()
        st.bar_chart(risk_counts)

# Run the dashboard
if __name__ == "__main__":
    display_dashboard()
