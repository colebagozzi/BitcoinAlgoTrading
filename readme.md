# Bitcoin Algorithmic Trading Bot

A basic automated Bitcoin trading bot that uses a simple moving average strategy.

## Setup

### Prerequisites
- Python 3.8+
- An account on a crypto exchange (Binance, Kraken, etc.)

### Installation

1. Install dependencies:
```bash
python -m pip install ccxt
```

2. Clone or navigate to the project directory:
```bash
cd BitcoinAlgoTrading
```

## Usage

### Configure API Credentials
Edit `trading.py` and add your exchange API credentials:
```python
bot = BitcoinTradingBot(exchange_name='binance', api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')
```

### Run the Bot
Uncomment the last line in `trading.py`:
```python
bot.run(check_interval=60)  # Check every 60 seconds
```

Then run:
```bash
python trading.py
```

## Files

- `trading.py` - Main trading bot implementation
- `TradingAlgo.py` - Base template
- `hello.py` - Test script

## Strategy

The bot uses a **Simple Moving Average Crossover** strategy:
- **Buy Signal**: When 5-period MA > 20-period MA
- **Sell Signal**: When 5-period MA < 20-period MA

## Warning

Always start with backtesting or paper trading before using real funds.