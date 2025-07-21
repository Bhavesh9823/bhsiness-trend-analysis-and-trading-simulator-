import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def download_data(symbol, start, end):
    return yf.download(symbol, start=start, end=end)

def generate_signals(df, short_window=20, long_window=50):
    df['Short_MA'] = df['Close'].rolling(window=short_window).mean()
    df['Long_MA'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = 0
    df.loc[df['Short_MA'] > df['Long_MA'], 'Signal'] = 1
    df.loc[df['Short_MA'] < df['Long_MA'], 'Signal'] = -1
    df['Position'] = df['Signal'].diff()
    return df

def simulate_trades(df, initial_capital=10000):
    capital = initial_capital
    position = 0
    portfolio_value = []
    buy_dates = []
    sell_dates = []

    for i in range(len(df)):
        price = df['Close'].iloc[i]
        signal = df['Position'].iloc[i]

        if signal == 1 and capital >= price:  # Buy signal
            position = capital // price
            capital -= position * price
            buy_dates.append(df.index[i])
        elif signal == -1 and position > 0:  # Sell signal
            capital += position * price
            position = 0
            sell_dates.append(df.index[i])

        current_value = capital + position * price
        portfolio_value.append(current_value)

    df['Portfolio Value'] = portfolio_value
    return df, buy_dates, sell_dates

def plot_results(df, buy_dates, sell_dates):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close Price', alpha=0.5)
    plt.plot(df['Short_MA'], label='Short MA', alpha=0.7)
    plt.plot(df['Long_MA'], label='Long MA', alpha=0.7)

    for date in buy_dates:
        plt.axvline(x=date, color='black', linestyle='--', alpha=0.5)
    for date in sell_dates:
        plt.axvline(x=date, color='red', linestyle='--', alpha=0.5)

    plt.title('Market Trend Analysis with Trade Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

    # Plot portfolio value
    plt.figure(figsize=(14, 5))
    plt.plot(df['Portfolio Value'], label='Portfolio Value', color='purple')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Value ($)')
    plt.grid()
    plt.legend()
    plt.show()

# === Main Run ===
if __name__ == "__main__":
    symbol = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2024-12-31'

    df = download_data(symbol, start_date, end_date)
    df = generate_signals(df)
    df, buys, sells = simulate_trades(df)
    plot_results(df, buys, sells)
