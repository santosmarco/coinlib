# coinlib
Coinlib is the ultimate cryptocurrency-related Python module. You can retrieve prices, market caps, 24h volumes and historical data for individual coins, or news and global data for the entire crypto universe with the use of simple and intuitive functions. 

# Installation
This module is specific to **Python 3**. Download it first [here](https://www.python.org/downloads/). The following installation instructions use the `pip install` command. If you are unfamiliar with it, check out [this tutorial](https://automatetheboringstuff.com/appendixa/).
## Windows
On terminal, type `pip install coinlib`
## MacOS / Linux
On Terminal, type `sudo pip3 install coinlib`

###### Note: `pip` installation has not been implemented yet.

# Documentation

## Getting started
First of all, you need to `import coinlib` into your project. For quick reference, the functions you can currently use from the library are listed below. Clicking on one of them will take you to its full documentation.
- [`get_coins(coins=[], convert='USD')`](https://github.com/santosmarco/coinlib#get_coinscoins-convertusd)
- [`get_global_data(convert='USD')`](https://github.com/santosmarco/coinlib#get_global_dataconvertusd)
- [`get_historical_data(coin, convert='USD', start=None, end=None)`](https://github.com/santosmarco/coinlib#get_historical_datacoin-convertusd-startnone-endnone)

## Conventions
###### Disclaimer
All pull requests MUST be consistent with these conventions.
###### coinlib.C1
All function parameters are case-INsensitive. Pass your arguments however you want: UPPERCASED, lowercased, or even CamelCased.
###### coinlib.C2
All function parameters that take coins as their argument accept either coin symbols, names or both. For example, you can pass Bitcoin to a function as `'btc'` or `'bitcoin'`.

## get_coins(coins=[], convert='USD')
`get_coins()` takes 2 optional parameters, `coins` and `convert`, and returns a dictionary with all available data for the specified coins. If no coin is specified, it returns a dictionary with all available data for all active coins.

###### >> Parameters
- `coins=[]`: Pass it a list of coin symbols, names, or both and it will return a dictionary containing data for the specified coins. Pass it nothing and it will return a dictionary containing data for all active coins. You can also pass it a string with only one coin symbol or name and it will return a data dictionary for this coin.
- `convert='USD'`: Pass it a string containing a currency symbol and it will return all data converted to this currency pair.
###### >> Returns
A dictionary in the form of:
```
{'btc': {'24h_volume': 6822060000.0,
         'available_supply': 16887562.0,
         'last_updated': datetime.datetime(2018, 2, 26, 11, 4, 28),
         'market_cap': 172947211198.0,
         'max_supply': 21000000.0,
         'name': 'Bitcoin',
         'percent_change_1h': 3.01,
         'percent_change_24h': 6.95,
         'percent_change_7d': -7.32,
         'price': 10241.1,
         'price_btc': 1.0,
         'rank': 1,
         'symbol': 'BTC',
         'total_supply': 16887562.0}}
```

###### Ex.1: To retrieve all coins data in a single dictionary
`get_coins()`
###### Ex.2: To retrieve data for Bitcoin
`get_coins('bitcoin')` or `get_coins('btc')`
###### Ex.3: To retrieve data for Bitcoin and Ethereum
`get_coins(['bitcoin', 'ethereum'])`, `get_coins(['btc', 'eth'])` or `get_coins(['bitcoin', 'eth'])`
###### Ex.4: To retrieve data for Bitcoin, Ethereum and Monero, all converted to Euro
`get_coins(['bitcoin', 'eth', 'xmr'], 'EUR')`
###### Ex.5: To retrieve Bitcoin's price directly
`get_coins('btc')['price']`
###### Ex.6: To retrieve Ethereum's market cap, in Australian Dollars, directly
`get_coins('eth', 'AUD')['market_cap']`

## get_global_data(convert='USD')
`get_global_data()` takes 1 optional parameter, `convert`, and returns a dictionary with all available data for the entire cryptocurrency market, properly converted to the specified conversion currency.

###### >> Parameters
- `convert='USD'`: Pass it a string containing a currency symbol and it will return all data converted to this currency pair.
###### >> Returns
A dictionary in the form of:
```
{'24h_volume': 18242464650.0,
 'active_assets': 585,
 'active_currencies': 903,
 'active_markets': 8718,
 'btc_dominance': 38.63,
 'last_updated': datetime.datetime(2018, 2, 26, 11, 19, 28),
 'market_cap': 452668330502.0}
```

###### Ex.1: To retrieve global data in US Dollars
`get_global_data()`
###### Ex.2: To retrieve global data in Euro
`get_global_data('EUR')`
###### Ex.3: To retrieve global market cap, in Euro, directly
`get_global_data('EUR')['market_cap']`

## get_historical_data(coin, convert='USD', start=None, end=None)
`get_historical_data()` takes 1 required parameter, `coin`, and 3 other optional parameters, `convert`, `start` and `end`, and returns a list of dictionaries, in which each dict in the list is the `coin` data for a single day, properly converted. The list includes all data from `start` date to `end` date.

###### >> Parameters
- `coin`: A coin symbol or name.
- `convert`: A conversion currency symbol (e.g. `'USD'`, `'EUR'`, `'AUD'`).
- `start`: A `datetime` object containing a start date (e.g. `datetime.datetime(2018, 2, 3, 0, 0, 0)` for Feb 3, 2018).
- `end`: A `datetime` object containing an end date.

###### >> Returns
A list of dictionaries in the form of:
```
[{'close': 8218.05,   # Day 1: Feb 3, 2018
  'high': 9400.99,
  'low': 7889.83,
  'open': 9251.27,
  'time': datetime.datetime(2018, 2, 3, 22, 0),
  'volumefrom': 164609.06,
  'volumeto': 1413207410.82},
 {'close': 6937.08,   # Day 2: Feb 4, 2018
  'high': 8391.29,
  'low': 6627.31,
  'open': 8218.05,
  'time': datetime.datetime(2018, 2, 4, 22, 0),
  'volumefrom': 341828.54,
  'volumeto': 2534149181.03},
 (...)]
```

###### Ex.1: To retrieve all historical data for Bitcoin, in US Dollars
`get_historical_data('btc')` or `get_historical_data('bitcoin')`
###### Ex.2: To retrieve historical data for Ethereum, in US dollars, from Feb 3, 2018 to today
`get_historical_data('eth', 'USD', datetime.datetime(2018, 2, 3, 0, 0, 0))`
###### Ex.3: To retrieve historical data for Monero, in Euro, from Feb 3, 2018 to Feb 15, 2018
```
>>> s = datetime.datetime(2018, 2, 3, 0, 0, 0)
>>> e = datetime.datetime(2018, 2, 15, 0, 0, 0)
>>> get_historical_data('monero', 'EUR', s, e)
```
