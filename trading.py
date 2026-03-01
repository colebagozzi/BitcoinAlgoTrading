import ccxt
import time
from datetime import datetime

class BitcoinTradingBot:
    def __init__(self, exchange_name='binance', api_key=None, api_secret=None):
        """Initialize the trading bot with exchange credentials"""
        self.exchange_class = getattr(ccxt, exchange_name)
        self.exchange = self.exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        self.symbol = 'BTC/USDT'
        self.position = None
        self.entry_price = None

    def get_price(self):
        """Fetch current Bitcoin price"""
        ticker = self.exchange.fetch_ticker(self.symbol)
        return ticker['last']

    def get_balance(self):
        """Get current account balance"""
        balance = self.exchange.fetch_balance()
        return {
            'btc': balance['BTC']['free'],
            'usdt': balance['USDT']['free']
        }

    def simple_strategy(self, price_history):
        """
        Simple moving average crossover strategy
        Buy when short MA > long MA, Sell when short MA < long MA
        """
        if len(price_history) < 20:
            return 'HOLD'

        short_ma = sum(price_history[-5:]) / 5
        long_ma = sum(price_history[-20:]) / 20

        if short_ma > long_ma and self.position is None:
            return 'BUY'
        elif short_ma < long_ma and self.position == 'LONG':
            return 'SELL'

        return 'HOLD'

    def place_order(self, action, amount):
        """Place a buy or sell order"""
        try:
            if action == 'BUY':
                order = self.exchange.create_market_buy_order(self.symbol, amount)
                self.position = 'LONG'
                self.entry_price = order['average']
                print(f"[{datetime.now()}] BUY ORDER: {amount} BTC @ {self.entry_price}")

            elif action == 'SELL':
                order = self.exchange.create_market_sell_order(self.symbol, amount)
                pnl = (order['average'] - self.entry_price) * amount
                print(f"[{datetime.now()}] SELL ORDER: {amount} BTC @ {order['average']} | PnL: {pnl}")
                self.position = None

            return order
        except Exception as e:
            print(f"Order failed: {e}")
            return None

    def run(self, check_interval=60):
        """Main trading loop"""
        price_history = []

        print("Bitcoin Trading Bot Started")
        print(f"Trading: {self.symbol}")

        try:
            while True:
                current_price = self.get_price()
                price_history.append(current_price)

                if len(price_history) > 100:
                    price_history.pop(0)

                signal = self.simple_strategy(price_history)
                balance = self.get_balance()

                print(f"[{datetime.now()}] Price: ${current_price} | Signal: {signal} | Position: {self.position}")

                # Execute trades based on signal
                if signal == 'BUY' and balance['usdt'] > 0:
                    trade_amount = 0.001  # Buy 0.001 BTC
                    self.place_order('BUY', trade_amount)

                elif signal == 'SELL' and self.position == 'LONG' and balance['btc'] > 0:
                    self.place_order('SELL', balance['btc'])

                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("Bot stopped by user")


if __name__ == '__main__':
    # Example: Replace with your actual API credentials
    bot = BitcoinTradingBot(exchange_name='binance', api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')
    # bot.run(check_interval=60)  # Check every 60 seconds

    # For testing without real trades:
    print("Trading bot created. Update API credentials and uncomment bot.run() to start trading.")
