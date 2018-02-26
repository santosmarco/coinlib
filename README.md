# coinlib
Coinlib is the ultimate cryptocurrency-related Python module. You can retrieve prices, market caps, 24h volumes and historical data for individual coins, or news and global data for the entire crypto universe with the use of simple and intuitive functions. 

# Installation
## Windows
`pip install coinlib`
## MacOS / Linux
`sudo pip3 install coinlib`

# Documentation

## Getting started
First of all, you need to `import coinlib` into your project. For quick reference, the functions you can currently use from the library are all listed below.
- `get_coins(coins=[], convert='USD')`
- `get_global_data(convert='USD')`
- `get_historical_data(coin, convert='USD', start=None, end=None)`

## Conventions
###### Disclaimer
All pull requests MUST be consistent with these conventions.
###### coinlib.C1
All function parameters are case-INsensitive. Pass your arguments however you want: UPPERCASED, lowercased, or even CamelCased.
###### coinlib.C2
All function parameters that take coins as their argument accept either coin symbols, names or both. You can pass them to the functions as `'btc'` or `'bitcoin'`.

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
Simply call `get_coins()`.
###### Ex.2: To retrieve data for Bitcoin
Call `get_coins('bitcoin')` or `get_coins('btc')`.
###### Ex.3: To retrieve data for Bitcoin and Ethereum
Call `get_coins(['bitcoin', 'ethereum'])`, `get_coins(['btc', 'eth'])` or `get_coins(['bitcoin', 'eth'])`.
###### Ex.4: To retrieve data for Bitcoin, Ethereum and Monero, all converted to Euro
Call `get_coins(['bitcoin', 'eth', 'xmr'], 'EUR')`.
###### Ex.5: To retrieve Bitcoin's price directly
Call `get_coins('btc')['price']`.
###### Ex.6: To retrieve Ethereum's market cap, in Australian Dollars, directly
Call `get_coins('eth', 'AUD')['market_cap']`.

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
Simply call `get_global_data()`.
###### Ex.2: To retrieve global data in Euro
Call `get_global_data('EUR')`.
###### Ex.3: To retrieve global market cap, in Euro, directly
Call `get_global_data('EUR')['market_cap']`.
