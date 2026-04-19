import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)

class BinanceTrader:
    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API Key and Secret must be provided.")

        # Initialize client for Binance.US
        self.client = Client(api_key, api_secret, tld='us')

    def get_symbol_info(self, symbol: str):
        """
        Fetches symbol information from Binance.
        """
        try:
            return self.client.get_symbol_info(symbol)
        except BinanceAPIException as e:
            logger.error(f"Error fetching info for {symbol}: {e}")
            return None

    def market_buy(self, symbol: str, quote_amount: float, dry_run: bool = False):
        """
        Executes a market buy order using the quote currency amount.

        Args:
            symbol: The trading pair (e.g., 'BTCUSD').
            quote_amount: The amount of quote currency to spend (e.g., 10.0 USD).
            dry_run: If True, only simulates the trade.
        """
        if dry_run:
            logger.info(f"[DRY RUN] Would market buy {quote_amount} USD/USDT worth of {symbol}")
            return {"symbol": symbol, "status": "DRY_RUN", "quoteOrderQty": quote_amount}

        try:
            # Using quoteOrderQty allows us to specify how much USD/USDT we want to spend
            order = self.client.order_market_buy(
                symbol=symbol,
                quoteOrderQty=quote_amount
            )
            logger.info(f"Successfully executed market buy for {symbol}: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API error during market buy for {symbol}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during market buy for {symbol}: {e}")
            raise
