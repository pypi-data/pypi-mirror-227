import pandas as pd
from DiscordAlertsTrader.calc_strat import calc_roi
# Define the value pattern
initial_val = 1
changes = [1 , 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2, 2.2, 2.25, 2.35, 2.25, 1.5, 1.25, 1.1, 1, 0.9, 0.8, 0.7, 0.6, 0.5 , .3, .25, .2]
quotes = [initial_val * change for change in changes]

quote = pd.Series(quotes)

PT = 2.25
SL = .25
roi = calc_roi(quote, PT,0.1, SL)
print(roi)

