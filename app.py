import pandas as pd
import streamlit as st

# File path for the stock data (ensure the file exists in the root directory)
file_path = 'merged_stock_data_with_categories_in_cells_nov2024.xlsx'

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

def calculate_risk_parameters(stock_symbols, file_path, risk_categories):
    """Calculates and categorizes risk parameters for a given stock portfolio."""
    df = pd.read_excel(file_path)
    results = []

    # Loop through each stock symbol provided
    for stock_symbol in stock_symbols:
        stock_info = df[df['Stock Symbol'] == stock_symbol]

        if stock_info.empty:
            st.write(f"No data found for stock symbol: {stock_symbol}")
            continue

        stock_info = stock_info.iloc[0]

        # Calculate risk parameters for the stock
        for category, parameters in risk_categories.items():
            for param, thresholds in parameters.items():
                value = stock_info.get(param)
                if value is not None:
                    risk_level = categorize_risk(value, thresholds)
                    description = get_parameter_description(param, risk_level)
                    results.append({
                        'Stock Symbol': stock_symbol,
                        'Category': category,
                        'Parameter': param,
                        'Value': value,
                        'Risk Level': risk_level,
                        'Description': description,
                        'Color': get_risk_color(risk_level)
                    })
                else:
                    results.append({
                        'Stock Symbol': stock_symbol,
                        'Category': category,
                        'Parameter': param,
                        'Value': 'Data not available',
                        'Risk Level': 'Data not available',
                        'Description': '',
                        'Color': 'black'
                    })

    # Convert the results to a pandas DataFrame
    results_df = pd.DataFrame(results)
    return results_df

def display_dashboard():
    st.title('Stock Risk Dashboard')

    # Read the stock data from the pre-defined Excel file
    df = pd.read_excel(file_path)

    # Get stock symbols input from the user
    stock_symbols = st.multiselect("Select Stock Symbols", df['Stock Symbol'].unique())
    
    if len(stock_symbols) > 0:
        # Define risk categories and parameters
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
        risk_data = calculate_risk_parameters(stock_symbols, file_path, risk_categories)

        # Display the results as a table
        st.write("Stock Risk Data", risk_data)

        # You can add more visualizations (e.g., pie chart, bar chart, etc.) if needed
        risk_counts = risk_data.groupby("Risk Level").size()
        st.bar_chart(risk_counts)

# Run the dashboard
if __name__ == "__main__":
    display_dashboard()
