import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def calculate_moving_averages():
    # Step 1: Scrape EUR/INR Data
    currency_pair = 'EURINR=X'
    start_date = '2023-08-25'
    end_date = '2024-08-25'
    data = yf.download(currency_pair, start=start_date, end=end_date)

    # Step 2: Calculate Moving Averages
    data['1-Day_MA'] = data['Close'].rolling(window=1).mean()
    data['1-Week_MA'] = data['Close'].rolling(window=5).mean()

    # Step 3: Predict Future Moving Averages for August-25-2024
    last_day_close = data['Close'].iloc[-1]
    predicted_1_day_ma = last_day_close

    last_week_closes = data['Close'].iloc[-5:]
    predicted_1_week_ma = last_week_closes.mean()

    # Step 4: Make Buy/Sell Decisions
    decision_1_day = 'NEUTRAL'
    if predicted_1_day_ma > predicted_1_week_ma:
        decision_1_day = 'BUY'
    elif predicted_1_day_ma < predicted_1_week_ma:
        decision_1_day = 'SELL'

    decision_1_week = 'NEUTRAL'
    if predicted_1_week_ma > predicted_1_day_ma:
        decision_1_week = 'BUY'
    elif predicted_1_week_ma < predicted_1_day_ma:
        decision_1_week = 'SELL'

    # Step 5: Store the Predictions in a DataFrame
    predictions = pd.DataFrame({
        'Predicted_1-Day_MA': [predicted_1_day_ma],
        'Predicted_1-Week_MA': [predicted_1_week_ma],
        'Decision_1-Day': [decision_1_day],
        'Decision_1-Week': [decision_1_week]
    })

    # Step 6: Save Decisions to CSV
    predictions.to_csv('moving_avg_decisions.csv', index=False)

    # Step 7: Plot the graph with moving averages and decision points
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='EUR/INR Close Price', linewidth=2)
    plt.plot(data.index, data['1-Day_MA'], label='1-Day MA', linestyle='--')
    plt.plot(data.index, data['1-Week_MA'], label='1-Week MA', linestyle='--')

    # Annotate Buy/Sell Decisions
    plt.annotate(f' {decision_1_day}', c='green', xy=(data.index[-1], last_day_close), xytext=(data.index[-1], last_day_close + 0.1))
    plt.annotate(f' {decision_1_week}', c='red', xy=(data.index[-1], last_week_closes.mean()), xytext=(data.index[-1], last_week_closes.mean() - 0.1))

    plt.title('EUR/INR Close Price and Moving Averages Decisions')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Step 8: Save the graph as an image
    plt.savefig('moving_avg_decisions.png')
    plt.show()


def calculate_bollinger_bands():
    # Step 1: Scrape EUR/INR Data
    currency_pair = 'EURINR=X'
    start_date = '2023-01-01'
    end_date = '2024-08-25'
    data = yf.download(currency_pair, start=start_date, end=end_date)

    # Step 2: Calculate Bollinger Bands for August-25-2024
    window = 5
    data['Middle_Band'] = data['Close'].rolling(window=window).mean()
    data['Upper_Band'] = data['Middle_Band'] + 2 * data['Close'].rolling(window=window).std()
    data['Lower_Band'] = data['Middle_Band'] - 2 * data['Close'].rolling(window=window).std()

    # Step 3: Calculate Bollinger Bands for August-26-2024
    # Assuming you have the closing prices for August-25-2024
    closing_price_aug_25 = data['Close'].iloc[-1]
    closing_prices_1_week = data['Close'].iloc[-5:]

    middle_band_1_day = closing_price_aug_25
    middle_band_1_week = closing_prices_1_week.mean()

    # Calculate the upper and lower bands for 1-day and 1-week based on your chosen standard deviation values

    # Step 4: Make Buy/Sell Decisions for August-25-2024 and one week from August-25-2024
    decision_1_day = 'NEUTRAL'
    decision_1_week = 'NEUTRAL'

    if closing_price_aug_25 > (middle_band_1_day + 2 * closing_prices_1_week.std()):
        decision_1_day = 'SELL'
    elif closing_price_aug_25 < (middle_band_1_day - 2 * closing_prices_1_week.std()):
        decision_1_day = 'BUY'

    if middle_band_1_week < (closing_prices_1_week.mean() - 2 * closing_prices_1_week.std()):
        decision_1_week = 'BUY'
    elif middle_band_1_week > (closing_prices_1_week.mean() + 2 * closing_prices_1_week.std()):
        decision_1_week = 'SELL'

    # Step 5: Store the Predictions in a DataFrame
    predictions = pd.DataFrame({
        'Predicted_1-Day': [middle_band_1_day],
        'Predicted_1-Week': [middle_band_1_week],
        'Decision_1-Day': [decision_1_day],
        'Decision_1-Week': [decision_1_week]
    })

    # Step 6: Save Decisions to CSV
    predictions.to_csv('eur_inr_bollinger_decisions.csv', index=False)

    # Convert the date to a datetime object
    date_1_day = datetime(2024, 8, 20)
    date_1_week = datetime(2024, 9, 1)

    # Step 7: Plot the graph with Bollinger Bands and Prediction Points
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='EUR/INR Close Price', color='blue')
    plt.plot(data.index, data['Middle_Band'], label='Middle Bollinger Band', color='orange')
    plt.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.4, label='Bollinger Bands')
    plt.scatter(date_1_day, middle_band_1_day, marker='o', color='green', label='1-Day Decision')
    plt.scatter(date_1_week, middle_band_1_week, marker='o', color='red', label='1-Week Decision')

    # Annotate Buy/Sell Decisions
    plt.text(date_1_day, middle_band_1_day, f'{decision_1_day}', ha='right', va='bottom', color='green')
    plt.text(date_1_week, middle_band_1_week, f'{decision_1_week}', ha='right', va='top', color='red')

    plt.title('EUR/INR Bollinger Bands and Decision')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    # Step 8: Save the graph as an image file
    plt.savefig('Bollinger_decisions.png')
    plt.show()


def calculate_cci():
    # Step 1: Scrape EUR/INR Data
    currency_pair = 'EURINR=X'
    start_date = '2023-01-01'
    end_date = '2024-08-25'
    data = yf.download(currency_pair, start=start_date, end=end_date)

    # Step 2: Calculate CCI for August-25-2024
    window = 20  # CCI period
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    mean_deviation = typical_price.rolling(window=window).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    cci = (typical_price - typical_price.rolling(window=window).mean()) / (0.015 * mean_deviation)

    # Step 3: Find the closest available date to August-25-2024
    target_date = datetime(2024, 8, 25)
    nearest_date = min(data.index, key=lambda x: abs(x - target_date))

    # Step 4: Calculate CCI for August 25, 2024
    cci_1_day = cci.loc[nearest_date]

    # Step 5: Calculate CCI for one week from August-25-2024
    cci_1_week = cci.loc[nearest_date:nearest_date + pd.DateOffset(weeks=1)]

    # Calculate the upper and lower thresholds for 1-day and 1-week based on your chosen values
    cci_threshold_1_day = 100
    cci_threshold_1_week = 100

    # Step 6: Make Buy/Sell Decisions for August-25-2024 and one week from August-25-2024
    decision_1_day = 'NEUTRAL'
    decision_1_week = 'NEUTRAL'

    if cci_1_day > cci_threshold_1_day:
        decision_1_day = 'SELL'
    elif cci_1_day < -cci_threshold_1_day:
        decision_1_day = 'BUY'

    if cci_1_week.mean() > cci_threshold_1_week:
        decision_1_week = 'SELL'
    elif cci_1_week.mean() < -cci_threshold_1_week:
        decision_1_week = 'BUY'

    # Step 7: Store the Predictions in a DataFrame
    predictions = pd.DataFrame({
        'Date': [nearest_date],
        'CCI_1-Day': [cci_1_day],
        'Decision_1-Day': [decision_1_day],
        'CCI_1-Week': [cci_1_week.mean()],
        'Decision_1-Week': [decision_1_week]
    })

    # Step 8: Save Decisions to CSV
    predictions.to_csv('cci_decisions.csv', index=False)

    # Step 9: Plot the graph with CCI and Decision Points
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, cci, label='CCI', color='blue')
    plt.axhline(y=100, color='red', linestyle='--', label='Overbought Threshold')
    plt.axhline(y=-100, color='green', linestyle='--', label='Oversold Threshold')

    # Annotate Buy/Sell Decisions
    plt.scatter(nearest_date, cci_1_day, marker='o', color='green', label='1-Day Decision')
    plt.scatter(nearest_date + pd.DateOffset(weeks=1), cci_1_week.mean(), marker='o', color='red', label='1-Week Decision')
    plt.annotate(f' {decision_1_day}', (nearest_date, cci_1_day), textcoords="offset points", xytext=(10, 10), ha='center', color='green')
    plt.annotate(f' {decision_1_week}', (nearest_date + pd.DateOffset(weeks=1), cci_1_week.mean()), textcoords="offset points", xytext=(10, 10), ha='center', color='red')

    plt.title('CCI with Buy/Sell Decisions')
    plt.xlabel('Date')
    plt.ylabel('CCI Value')
    plt.legend()
    plt.grid()

    # Step 10: Save the graph as an image file
    plt.savefig('cci_decisions.png')
    plt.show()


def main():
    calculate_moving_averages()
    calculate_bollinger_bands()
    calculate_cci()

if __name__ == '__main__':
    main()
