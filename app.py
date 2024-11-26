import pandas as pd

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
        # (The description dictionary goes here)
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
            print(f"No data found for stock symbol: {stock_symbol}")
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

    # Display the results in an HTML format
    html_output = results_df.to_html(index=False, escape=False, 
                                      formatters={
                                          'Risk Level': lambda x: f"<span style='color:{get_risk_color(x)}'>{x}</span>",
                                          'Value': lambda x: str(x),
                                      })
    print(html_output)

def add_new_stock():
    """Prompt the user to add a new stock symbol."""
    stock_symbol = input("Enter the new stock symbol: ").strip()
    return stock_symbol

def add_new_risk_category(risk_categories):
    """Allow the user to add a new risk category and parameters."""
    category_name = input("Enter the name of the new risk category: ").strip()
    risk_categories[category_name] = {}
    
    while True:
        param_name = input("Enter a new parameter name (or type 'done' to finish): ").strip()
        if param_name.lower() == 'done':
            break
        
        min_value = float(input(f"Enter the minimum value for {param_name}: "))
        max_value = float(input(f"Enter the maximum value for {param_name}: "))
        risk_categories[category_name][param_name] = (min_value, max_value)
        
    print(f"Added new category '{category_name}' with parameters: {risk_categories[category_name]}")
    return risk_categories

# Example usage
if __name__ == "__main__":
    stock_symbols = input("Enter stock symbols separated by commas: ").split(',')
    stock_symbols = [symbol.strip() for symbol in stock_symbols]

    # Define the initial risk categories
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

    # Prompt to add more stocks
    while True:
        more_stocks = input("Would you like to add more stocks? (yes/no): ").strip().lower()
        if more_stocks == 'yes':
            new_stock = add_new_stock()
            stock_symbols.append(new_stock)
        elif more_stocks == 'no':
            break
        else:
            print("Please enter 'yes' or 'no'.")

    # Prompt to add more risk categories
    while True:
        add_category = input("Would you like to add a new risk category? (yes/no): ").strip().lower()
        if add_category == 'yes':
            risk_categories = add_new_risk_category(risk_categories)
        elif add_category == 'no':
            break
        else:
            print("Please enter 'yes' or 'no'.")

    # Path to the Excel file
    file_path = "merged_stock_data_with_categories_in_cells_nov2024.xlsx"  # Make sure the file path is correct
    calculate_risk_parameters(stock_symbols, file_path, risk_categories)
