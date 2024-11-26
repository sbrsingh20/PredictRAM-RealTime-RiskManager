import pandas as pd
import streamlit as st

# File path for the Excel file containing the new data
file_path = 'India Inflation CPI Consumer Price Index_IncomeStatement_correlation_results.xlsx'

# Function to display data for selected stocks from the new Excel file
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

        # Optionally, you can call the risk calculation functions and display those results too
        # Example: Display risk data
        risk_categories = {
            "Market Risk": {
                "Volatility": (0.1, 0.2),
                "Beta": (0.5, 1.5),
                "Correlation with ^NSEI": (0.7, 1),
            },
            "Financial Risk": {
                "debtToEquity": (0.5, 1.5),
                "currentRatio": (1.5, 2),
                "quickRatio": (1, 1.5),
                "Profit Margins": (20, 30),
                "returnOnAssets": (10, 20),
                "returnOnEquity": (15, 25),
            },
            "Liquidity Risk": {
                "Volume": (1_000_000, float('inf')),
                "Average Volume": (500_000, 1_000_000),
                "marketCap": (10_000_000_000, float('inf')),
            },
            "Credit Risk": {
                "totalDebt": (0, float('inf')),
                "debtToEquity": (0.5, 1.5),
            },
            "Operational Risk": {
                "Profit Margins": (20, 30),
                "CAGR": (20, 30),
            },
            "Portfolio Risk": {
                "Maximum Drawdown": (15, 30),
                "Annualized Volatility (%)": (15, 25),
                "Sharpe Ratio": (1.5, float('inf')),
                "Treynor Ratio": (0.2, float('inf')),
                "Sortino Ratio": (2, float('inf')),
                "VaR (95%)": (0, 10),
            },
            "Industry Risk": {
                "industry_debtToEquity": (0.5, 1.5),
                "industry_returnOnAssets": (10, 20),
                "industry_returnOnEquity": (15, 25),
                "industry_profitMargins": (20, 30),
                "industry_revenueGrowth": (5, 15),
                "industry_currentRatio": (1.5, 2),
                "industry_quickRatio": (1, 1.5),
                "industry_ebitda": (10, 20),
                "industry_totalDebt": (0, float('inf')),
                "industry_grossMargins": (20, 30),
                "industry_ebitdaMargins": (15, 25),
                "industry_operatingMargins": (15, 25),
            },
            "Other Risks": {
                "Dividend Payout Ratio": (0.4, 0.6),
                "Dividend Yield": (5, float('inf')),
            }
        }

        # Calculate the risk data for the selected stocks
        # risk_data = calculate_risk_parameters(stock_symbols, file_path, risk_categories)

        # Display the results as a table (This could be part of the other section for risk categories)
        # st.write("Stock Risk Data", risk_data)

# Run the dashboard
if __name__ == "__main__":
    display_dashboard()
