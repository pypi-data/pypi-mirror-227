# StockHero  
## Download market data from finance APIs and other sources
> It's an open-source tool that uses publicly available APIs and other sources, and is intended for research and educational purposes only.<br>
> If you find a bug, try fix it yourself first
  
[![Downloads](https://static.pepy.tech/badge/StockHero)](https://pepy.tech/project/StockHero)

## New Features in 0.4.8
* Minor fixes

### New Features planned for the next release
- fix more "features" (bugs)

## The Ticker module
The ```Ticker``` module, gets the financial data from nasdaq.com, morningstar.com, yahoo.com as a pandas.DataFrame <br>

```python

import StockHero as stock
nvda = stock.Ticker('NVDA') # e.g. NVIDIA Corp
#or
nvda = stock.Ticker('US67066G1040') # e.g. NVIDIA Corp

''' Morningstar '''
nvda.morningstar.quote                  # Quote
nvda.morningstar.key_statistics         # Key Statistics (combination of the ones below)
nvda.morningstar.growth_rev             # Growth - Revenue %
nvda.morningstar.growth_op_inc          # Growth - Operating Income %
nvda.morningstar.growth_net_inc         # Growth - Net Income %
nvda.morningstar.growth_eps             # Growth - EPS %

''' Yahoo Finance '''
## I would recommend to use yfinance instead of this library ##

nvda.yahoo.statistics                   # Statistics
nvda.yahoo.statistics_p                 # Statistics - PreProcessed

''' NASDAQ '''
nvda.nasdaq.summ                        # Summary
nvda.nasdaq.div_hist                    # Dividend History
nvda.nasdaq.hist_quotes_stock           # Historical Quotes for Stocks
nvda.nasdaq.hist_quotes_etf             # Historical Quotes for ETFs
nvda.nasdaq.hist_nocp                   # Historical Nasdaq Official Closing Price (NOCP)
nvda.nasdaq.fin_income_statement_y      # Financials - Income Statement - Yearly
nvda.nasdaq.fin_balance_sheet_y         # Financials - Balance Sheet    - Yearly
nvda.nasdaq.fin_cash_flow_y             # Financials - Cash Flow        - Yearly
nvda.nasdaq.fin_fin_ratios_y            # Financials - Financial Ratios - Yearly
nvda.nasdaq.fin_income_statement_q      # Financials - Income Statement - Quarterly
nvda.nasdaq.fin_balance_sheet_q         # Financials - Balance Sheet    - Quarterly
nvda.nasdaq.fin_cash_flow_q             # Financials - Cash Flow        - Quarterly
nvda.nasdaq.fin_fin_ratios_q            # Financials - Financial Ratios - Quarterly
nvda.nasdaq.earn_date_eps               # Earnings Date - Earnings Per Share
nvda.nasdaq.earn_date_surprise          # Earnings Date - Quarterly Earnings Surprise Amount
nvda.nasdaq.yearly_earn_forecast        # Earnings Date - Yearly Earnings Forecast 
nvda.nasdaq.quarterly_earn_forecast     # Earnings Date - Quarterly Earnings Forecast 
nvda.nasdaq.pe_peg_forecast             # Price/Earnings, PEG Ratios, Growth Rates Forecast

''' Gurufocus '''
nvda.gurufocus.pe_ratio_av              # Historical Average Price/Earnings-Ratio
nvda.gurufocus.debt_to_ebitda           # Debt-to-EBITDA Ratio
```

## The StockExchange module
The ```StockExchange``` module, gets the financial data from the NASDAQ Stock Screener <br>
Added CNN Fear and Greed Index

```python
import StockHero as stock
t = stock.StockExchange('something') # e.g. Nasdaq

''' NASDAQ '''
t.nasdaq                              # Nasdaq Stock Market

''' CNN '''
t.cnn_fear_and_greed                  # CNN Fear and Greed Index
```

## Combining both modules
You can combine both modules, for example
```python
import StockHero as stock
t = stock.StockExchange('something')
df = t.nasdaq
ticker = df.loc[df['Name'].str.contains('NVIDIA'), 'Symbol'].values[0]
n = stock.Ticker(ticker)
n.morningstar_quote
```

### Legal Stuff
StockHero is distributed under the Apache Software License
<br>
### Any feedback or suggestions, let me know
Or in the words of Peter Thiel:
> We wanted flying cars, instead we got 140 characters
<br>
### Versions

0.4.8  Minor fixes <br>
... <br>
0.0.1  First Release