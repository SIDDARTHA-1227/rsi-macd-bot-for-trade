import time
import yfinance as yf
import requests
from datetime import datetime
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

# === CONFIGURATION ===
BOT_TOKEN = '8273974258:AAHlgCMDjBVp4FlZHvoo_6unCeNQ4uMxjUk'
USER_ID = '6103387176'
ASSET = 'BITCOIN'
TICKER = 'BTC-USD'  # Can be changed to any other valid ticker like 'ETH-USD', 'EURUSD=X', etc.
INTERVAL_SECONDS = 60  # 1-minute interval

def fetch_price_data():
    try:
        df = yf.download(tickers=TICKER, period='1d', interval='1m', auto_adjust=False, progress=False)
        return df
    except Exception as e:
        print(f"⚠️ Error fetching data: {e}")
        return pd.DataFrame()

def analyze(df):
    if df.empty or 'Close' not in df.columns:
        return None, None

    try:
        close_series = pd.Series(df['Close'].values.ravel(), index=df.index)
        df['RSI'] = RSIIndicator(close=close_series, window=14).rsi()
        macd = MACD(close=close_series, window_slow=26, window_fast=12, window_sign=9)
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df.dropna(inplace=True)

        if len(df) < 2:
            return None, None

        last = df.iloc[-1]
        prev = df.iloc[-2]

        price = last['Close'].item()
        rsi = last['RSI'].item()
        macd_val = last['MACD'].item()
        signal_val = last['MACD_Signal'].item()
        prev_price = prev['Close'].item()

        print(f"[DEBUG] RSI: {rsi:.2f}, MACD: {macd_val:.4f}, Signal: {signal_val:.4f}, Price: {price:.4f}")

        signal = None
        # ✅ Flexible & Frequent Signal Strategy
        if rsi < 45 and macd_val > signal_val:
            signal = 'UP'
        elif rsi > 55 and macd_val < signal_val:
            signal = 'DOWN'
        elif 45 <= rsi <= 55:
            if price > prev_price:
                signal = 'UP'
            elif price < prev_price:
                signal = 'DOWN'

        return signal, round(price, 4)

    except Exception as e:
        print(f"⚠️ Indicator calculation error: {e}")
        return None, None

def send_signal(signal, price):
    now = datetime.now().strftime("%I:%M %p")
    icon = '🔼 BUY' if signal == 'UP' else '🔽 SELL'
    message = (
        f"🔔 Signal Alert - Relaxed Triple Threat Strategy\n"
        f"Asset: {ASSET}\n"
        f"Action: {icon}\n"
        f"Price: {price}\n"
        f"Time: {now}"
    )
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(url, data={'chat_id': USER_ID, 'text': message})
        if response.status_code == 200:
            print(f"[{now}] ✅ Signal sent: {signal} | Price: {price}")
        else:
            print(f"❌ Telegram error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")

def run_bot():
    print("🟢 RSI + MACD Telegram Bot Running... (Relaxed Triple Threat Strategy)")
    while True:
        try:
            df = fetch_price_data()
            signal, price = analyze(df)
            if signal:
                send_signal(signal, price)
            else:
                print(f"[{datetime.now().strftime('%I:%M %p')}] ⏸️ No valid signal now.")
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user.")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run_bot()  