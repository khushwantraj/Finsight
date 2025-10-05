"""Example usage of AlphaVantage connector."""

import os
from dotenv import load_dotenv
from finsight.connectors.factory import ConnectorFactory

# Load environment variables
load_dotenv()


def main():
    """Demonstrate AlphaVantage connector usage."""
    
    # Create AlphaVantage connector
    credentials = {
        'api_key': os.getenv('ALPHA_VANTAGE_API_KEY')
    }
    
    if not credentials['api_key']:
        print("Please set ALPHA_VANTAGE_API_KEY in .env file")
        return
    
    av = ConnectorFactory.create('alphavantage', credentials)
    
    # Get stock quote
    print("Getting stock quote for AAPL...")
    result = av.get_quote('AAPL')
    
    if result.status.value == 'success':
        quote = result.data['quote']
        print(f"\nQuote: {quote}")
    else:
        print(f"Error: {result.error}")
    
    # Get intraday data
    print("\nGetting intraday data for AAPL...")
    result = av.get_intraday('AAPL', interval='5min')
    
    if result.status.value == 'success':
        data = result.data['data']
        print(f"Retrieved {len(data)} data points")
        # Print first data point
        if data:
            first_key = list(data.keys())[0]
            print(f"Latest: {first_key} -> {data[first_key]}")
    else:
        print(f"Error: {result.error}")
    
    # Get company overview
    print("\nGetting company overview for AAPL...")
    result = av.get_company_overview('AAPL')
    
    if result.status.value == 'success':
        overview = result.data['overview']
        print(f"Company: {overview.get('Name')}")
        print(f"Sector: {overview.get('Sector')}")
        print(f"Industry: {overview.get('Industry')}")
        print(f"Market Cap: {overview.get('MarketCapitalization')}")
    else:
        print(f"Error: {result.error}")


if __name__ == '__main__':
    main()
