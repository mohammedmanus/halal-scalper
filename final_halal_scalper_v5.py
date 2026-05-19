import ccxt
import time
import pandas as pd

import os

# قراءة الإعدادات من متغيرات البيئة (للأمان في GitHub Actions)
api_key = os.getenv('BINANCE_API_KEY', 'jFNT6VjjsGiWR6RpkcMVDBXzSobyW9R23HwkCjEJX4NRuQBm81klgebukeTmAkZR')
api_secret = os.getenv('BINANCE_SECRET', 'dgxNIARpeEqeYoc1jw21QbUc7uhgM5ItmwZsoFgTBNAwQ14DlHrZQAoI6tRoJJ7z')
proxy_url = os.getenv('PROXY_URL', 'http://mohameedhameed_gmail_com-country-de-sid-d1f2c3c2f8454-filter-medium:dkcf3uhx1f@gate.nodemaven.com:8080')

proxy_config = {
    'http': proxy_url,
    'https': proxy_url
}

# إعداد Binance مع البروكسي
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'proxies': proxy_config
})

# قائمة العملات الحلال (تم التحقق منها سابقاً)
HALAL_COINS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT', 'MATIC/USDT', 'ENJ/USDT', 'ONDO/USDT']

def get_balance():
    try:
        balance = exchange.fetch_balance()
        return balance['total']['USDT']
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0

def open_position(symbol, amount_usdt):
    try:
        print(f"Opening position for {symbol} with {amount_usdt} USDT...")
        order = exchange.create_market_buy_order(symbol, amount_usdt)
        print(f"Order filled: {order['id']}")
        return order
    except Exception as e:
        print(f"Error opening position for {symbol}: {e}")
        return None

def main():
    print("Starting Fast Halal Scalper v5 with NodeMaven Proxy...")
    total_usdt = get_balance()
    print(f"Total USDT Balance: {total_usdt}")
    
    if total_usdt < 10:
        print("Insufficient balance.")
        return

    # توزيع الرصيد: 10-15% لكل صفقة
    trade_amount = total_usdt * 0.12 # متوسط 12%
    
    # البحث عن أفضل فرص حالياً (أكثر العملات تذبذباً في الـ 24 ساعة الماضية)
    tickers = exchange.fetch_tickers(HALAL_COINS)
    sorted_tickers = sorted(tickers.items(), key=lambda x: abs(x[1]['percentage']), reverse=True)
    
    opened_count = 0
    for symbol, ticker in sorted_tickers:
        if opened_count >= 5: # فتح 5 صفقات كحد أقصى لتوزيع المخاطر
            break
            
        print(f"Analyzing {symbol}: Change {ticker['percentage']}%")
        # استراتيجية بسيطة: الشراء عند الزخم الإيجابي القوي
        if ticker['percentage'] > 2: 
            order = open_position(symbol, trade_amount)
            if order:
                opened_count += 1
                time.sleep(1) # تجنب الـ Rate Limit

if __name__ == "__main__":
    main()
