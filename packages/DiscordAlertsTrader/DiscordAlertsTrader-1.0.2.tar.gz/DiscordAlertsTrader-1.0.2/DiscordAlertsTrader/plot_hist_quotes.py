"""get livequotes from algo_1f"""
import pandas as pd
from datetime import datetime

live_quotes_p = "data/live_quotes/"

port= pd.read_csv("data/analysts_portfolio.csv")

trades = port[(port['Date']>'2023-06-02') & (port['Channel']=='fend_bot')]

for ix, row in trades.iterrows():
    try:
        quotes = pd.read_csv(live_quotes_p + row['Symbol'] + ".csv")
    except FileNotFoundError:
        continue
    
    dates = quotes['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
    msk = dates >= pd.to_datetime(row['Date'])
    quotes['Date'] = dates
    quotes.drop('timestamp', axis=1, inplace=True)
    quotes = quotes[msk].set_index( 'Date', drop=True)
    quotes.index = pd.to_datetime(quotes.index)
    quotes.plot(y=' quote')

    quotes.plot(' quote')
        
    df = df[df['Date'] > row['Date']]
    df = df[df['Date'] < row['CloseTime']]
    df['PnL'] = (df['Last'] - row['Price'])/row['Price'] * 100
    df['PnL'].plot()
    df['Last'].plot()
    df['Bid'].plot()
    df['Ask'].plot()
    df['Volume'].plot()
    df['OpenInterest'].plot()
    df['IV'].plot()
    df['Delta'].plot()
    df['Gamma'].plot()
    df['Theta'].plot()
    df['Vega'].plot()