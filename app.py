import pandas as pd
import yfinance as yf
import streamlit as st

# File path for the stock data and inflation data (ensure the file exists in the root directory)
file_path = 'India Inflation CPI Consumer Price Index_IncomeStatement_correlation_results.xlsx'

# Define the categorization function and helper methods
def categorize_risk(value, thresholds):
    """Categorizes risk based on predefined thresholds."""
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
    """Returns the description for a given risk parameter based on risk level."""
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
        # Add similar descriptions for other parameters as needed
    }
    return descriptions.get(param, {}).get(risk_level, "No description available.")

def get_risk_color(risk_level):
    """Returns the color associated with a risk level."""
    if risk_level == "Good":
        return "green"
    elif risk_level == "Neutral":
        return "yellow"
    elif risk_level == "Bad":
        return "red"
    else:
        return "black"

# Function to calculate correlation with inflation using yfinance
def get_inflation_correlation(stock_symbol):
    inflation_data = {
        "Sep-22": 6.488240065, "Oct-22": 6.084867894, "Nov-22": 5.409705648, "Dec-22": 5.502392344,
        "Jan-23": 6.155075939, "Feb-23": 6.16, "Mar-23": 5.793650794, "Apr-23": 5.090054816, "May-23": 4.418604651,
        "Jun-23": 5.572755418, "Jul-23": 7.544264819, "Aug-23": 6.912442396, "Sep-23": 5.02, "Oct-23": 4.87,
        "Nov-23": 5.55, "Dec-23": 5.69, "Jan-24": 5.1, "Feb-24": 5.09, "Mar-24": 4.85, "Apr-24": 4.83,
        "May-24": 4.75, "Jun-24": 5.08, "Jul-24": 3.54, "Aug-24": 3.65, "Sep-24": 5.49
    }
    
    # Fetch stock data for the selected stock symbol
    stock_symbol_ns = stock_symbol + ".NS"  # Append ".NS" for Indian stocks
    stock_data = yf.download(stock_symbol_ns, start="2022-09-01", end="2024-09-30", progress=False)
    
    # If stock data is empty or insufficient
    if stock_data.empty:
        return "No data available"
    
    # Compute correlation with inflation (monthly returns)
    inflation_series = pd.Series(inflation_data)
    stock_monthly_returns = stock_data['Adj Close'].resample('M').ffill().pct_change().dropna()
    
    # Align both data series by their index (date)
    aligned_data = pd.concat([stock_monthly_returns, inflation_series], axis=1).dropna()
    aligned_data.columns = ['Stock Return', 'Inflation']
    
    # Calculate correlation
    correlation = aligned_data['Stock Return'].corr(aligned_data['Inflation'])
    
    return correlation

# Function to display financial data for selected stocks
def display_income_statement_data(selected_stocks):
    # Read the data from the Excel file
    df = pd.read_excel(file_path)

    # Check if the selected stock exists in the data and filter it
    filtered_data = df[df['Stock Name'].isin(selected_stocks)]

    if filtered_data.empty:
        st.write("No data found for the selected stocks.")
    else:
        # Display the filtered data in a readable table format
        st.write("Selected Stock Data", filtered_data[['Stock Name',
                                                       'June 2024 Total Revenue/Income',
                                                       'June 2024 Total Operating Expense',
                                                       'June 2024 Operating Income/Profit',
                                                       'June 2024 EBITDA',
                                                       'June 2024 EBIT',
                                                       'June 2024 Income/Profit Before Tax',
                                                       'June 2024 Net Income From Continuing Operation',
                                                       'June 2024 Net Income',
                                                       'June 2024 Net Income Applicable to Common Share',
                                                       'June 2024 EPS (Earning Per Share)',
                                                       'Correlation with Total Revenue/Income',
                                                       'Correlation with Total Operating Expense',
                                                       'Correlation with Operating Income/Profit',
                                                       'Correlation with EBITDA',
                                                       'Correlation with EBIT',
                                                       'Correlation with Income/Profit Before Tax',
                                                       'Correlation with Net Income From Continuing Operation',
                                                       'Correlation with Net Income',
                                                       'Correlation with Net Income Applicable to Common Share',
                                                       'Correlation with EPS (Earning Per Share)']])

# Create a function to display the Streamlit dashboard
def display_dashboard():
    st.title('Stock Risk Dashboard')

    # Read the stock data from the pre-defined Excel file for the risk categories
    df = pd.read_excel(file_path)

    # Get stock symbols input from the user
    stock_symbols = st.multiselect("Select Stock Symbols", df['Stock Name'].unique())

    if len(stock_symbols) > 0:
        # Display data for the selected stocks
        display_income_statement_data(stock_symbols)

        # Display correlation of selected stocks with inflation
        st.write("Stock Correlation with Inflation:")
        for stock_symbol in stock_symbols:
            correlation = get_inflation_correlation(stock_symbol)
            st.write(f"{stock_symbol}: {correlation}")

# Run the dashboard
if __name__ == "__main__":
    display_dashboard()
