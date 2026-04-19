# Binance.US Automated Daily Trader

A production-ready Python application that performs automated daily cryptocurrency purchases using the Binance.US API.

## 🚀 Features

*   **Automated Purchases**: Designed to be run via cron for daily DCA (Dollar Cost Averaging).
*   **Binance.US Support**: Uses the official `python-binance` library with Binance.US endpoints.
*   **Safety First**:
    *   Validation of trading pairs and amounts.
    *   Idempotency guard to prevent duplicate trades within the same minute.
    *   Dry-run mode for testing configurations.
    *   Retry logic with exponential backoff for API calls.
*   **Production Ready**:
    *   Logging to both console and file.
    *   Secrets managed via `.env` file.
    *   Modular and extensible code structure.

## 📁 Project Structure

```
project/
├── trader.py            # Main entry point
├── binance_client.py    # Binance API wrapper
├── config.json          # User-defined purchase rules
├── .env.example         # Template for environment variables
├── requirements.txt     # Project dependencies
├── logs/
│   └── trades.log       # Execution logs
├── utils/
│   └── pair_utils.py    # Trading pair normalization logic
└── README.md
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Binance.US API Key and Secret:

```
BINANCE_API_KEY=your_actual_api_key
BINANCE_API_SECRET=your_actual_api_secret
```

**Security Note:** Use an API key with "Enable Spot Trading" checked and "Enable Withdrawals" UNCHECKED.

### 3. Configure Purchase Rules

Edit `config.json` to define your daily purchases:

```json
{
  "purchases": [
    { "pair": "BTC/USD", "amount": 10 },
    { "pair": "ETH/USDT", "amount": 10 }
  ]
}
```

*   `pair`: Must be in `BASE/QUOTE` format. Supported quotes: `USD`, `USDT`.
*   `amount`: The amount of quote currency to spend.

## 🏃 Usage

### Dry Run (Recommended for first time)

Simulate trades without actually executing them:

```bash
python trader.py --dry-run
```

### Regular Execution

```bash
python trader.py
```

## ⏰ Automation with Cron

To run the trader daily (e.g., at 9:00 AM), add a cron job:

```bash
0 9 * * * cd /path/to/project && /usr/bin/python3 trader.py >> logs/trades.log 2>&1
```

## 📝 Logging

All activities are logged to `logs/trades.log`. You can monitor the progress with:

```bash
tail -f logs/trades.log
```
