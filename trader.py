import os
import sys
import json
import logging
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv
from binance_client import BinanceTrader
from utils.pair_utils import normalize_pair
from binance.exceptions import BinanceAPIException

# Configure logging
LOG_FILE = "logs/trades.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

LAST_RUN_FILE = ".last_run"

def check_idempotency():
    """
    Check if the script has already run in the current minute.
    """
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            last_run_str = f.read().strip()
            if last_run_str:
                last_run = datetime.fromisoformat(last_run_str)
                now = datetime.now()
                if last_run.year == now.year and last_run.month == now.month and \
                   last_run.day == now.day and last_run.hour == now.hour and \
                   last_run.minute == now.minute:
                    logger.info("Script already executed in this minute. Exiting safely.")
                    return False
    return True

def update_last_run():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(datetime.now().isoformat())

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)

def run_trade_with_retry(trader, symbol, amount, dry_run, max_retries=3):
    retries = 0
    while retries <= max_retries:
        try:
            return trader.market_buy(symbol, amount, dry_run=dry_run)
        except BinanceAPIException as e:
            if retries == max_retries:
                logger.error(f"Failed to execute trade for {symbol} after {max_retries} retries: {e}")
                raise

            wait_time = 2 ** retries # 1, 2, 4
            logger.warning(f"Trade failed for {symbol}, retrying in {wait_time}s... (Error: {e})")
            time.sleep(wait_time)
            retries += 1
        except Exception as e:
            logger.error(f"Unexpected error for {symbol}: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Binance.US Automated Trader")
    parser.add_argument("--dry-run", action="store_true", help="Simulate trades without executing")
    args = parser.parse_args()

    if not check_idempotency():
        return

    update_last_run()

    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("BINANCE_API_KEY or BINANCE_API_SECRET missing in environment.")
        sys.exit(1)

    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

    trader = BinanceTrader(api_key, api_secret)

    for purchase in config.get("purchases", []):
        pair = purchase.get("pair")
        amount = purchase.get("amount")

        if not pair or amount is None or amount <= 0:
            logger.error(f"Invalid purchase config: {purchase}")
            continue

        try:
            symbol = normalize_pair(pair)
        except ValueError as e:
            logger.error(f"Error normalizing pair {pair}: {e}")
            continue

        # Validate symbol exists on Binance
        symbol_info = trader.get_symbol_info(symbol)
        if not symbol_info:
            logger.error(f"Symbol {symbol} not found on Binance. Skipping.")
            continue

        logger.info(f"Processing trade: {pair} ({symbol}) for {amount}")

        try:
            run_trade_with_retry(trader, symbol, amount, args.dry_run)
        except Exception:
            # Error already logged in run_trade_with_retry
            continue

if __name__ == "__main__":
    main()
