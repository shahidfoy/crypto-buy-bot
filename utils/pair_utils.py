def normalize_pair(pair: str) -> str:
    """
    Normalizes and validates a trading pair.

    Args:
        pair: A string like "BTC/USD" or "ETH/USDT".

    Returns:
        The normalized pair string for Binance (e.g., "BTCUSD").

    Raises:
        ValueError: If the pair format is invalid or the quote currency is not supported.
    """
    if not isinstance(pair, str):
        raise ValueError(f"Pair must be a string, got {type(pair).__name__}")

    if '/' not in pair:
        raise ValueError(f"Invalid pair format: '{pair}'. Must contain '/' (e.g., 'BTC/USD').")

    parts = pair.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid pair format: '{pair}'. Must have exactly one '/'.")

    base, quote = [part.strip().upper() for part in parts]

    if not base or not quote:
        raise ValueError(f"Invalid pair format: '{pair}'. Base and quote must not be empty.")

    if quote not in ["USD", "USDT"]:
        raise ValueError(f"Unsupported quote currency: '{quote}'. Only USD and USDT are supported.")

    return f"{base}{quote}"
