import json
import requests
import datetime
import news
import wallet


VALID_CONVERSION_CURRENCIES = [
    "USD", "BRL", "CAD", "CHF",
    "CLP", "CNY", "CZK", "DKK",
    "EUR", "GBP", "HKD", "HUF",
    "IDR", "ILS", "INR", "JPY",
    "KRW", "MXN", "MYR", "NOK",
    "NZD", "PHP", "PKR", "PLN",
    "RUB", "SEK", "SGD", "THB",
    "TRY", "TWD", "ZAR", "AUD"
    ]


def errors(error_code, error_info=['', '']):
    errors = {
        '101': (f'[Error 101] Invalid conversion currency: {error_info[0]}. '
                + 'Valid conversion currencies are: '
                + '{}'.format(', '.join(VALID_CONVERSION_CURRENCIES))),
        '102': ('[Error 102] Unable to retrieve online data. '
                + 'Either your Internet connection or www.coinmarketcap.com '
                + 'is down.'),
        '103': f'[Error 103] Invalid symbol/name: {error_info[0]}.',
        '104': ('[Error 104] Unable to retrieve online data. '
                + 'Either your Internet connection or '
                + 'www.min-api.cryptocompare.com is down.'),
        '105': ('[Error 105] "start" and "end" parameters should be datetime '
                + 'objects.')
        }
    return errors[error_code]


def pull_coins_data(convert='USD'):
    convert = convert.upper().strip()
    url = ('https://api.coinmarketcap.com/v1/ticker/'
           + f'?convert={convert}&limit=0')
    raw_data = requests.get(url)
    try:
        raw_data.raise_for_status()
    except Exception:
        raise RuntimeError(errors('102'))
    formatted_data = json.loads(raw_data.text)
    return formatted_data


def pull_global_data(convert='USD'):
    convert = convert.upper().strip()
    url = f'https://api.coinmarketcap.com/v1/global/?convert={convert}'
    raw_data = requests.get(url)
    try:
        raw_data.raise_for_status()
    except Exception:
        raise RuntimeError(errors('102'))
    formatted_data = json.loads(raw_data.text)
    return formatted_data


def pull_historical_data(coin, convert='USD'):
    convert = convert.upper().strip()
    coin = coin.lower().strip()
    if coin not in get_all_coins_by_symbol():
        coins_by_name = get_all_coins_by_name()
        if coin in coins_by_name:
            coin = coins_by_name[coin]['symbol']
        else:
            raise ValueError(errors('103', [coin]))
    else:
        coin = coin.upper()
    url = ('https://min-api.cryptocompare.com/data/'
           + f'histoday?fsym={coin}&tsym={convert}'
           + '&limit=8000&aggregate=1&e=CCCAGG')
    raw_data = requests.get(url)
    try:
        raw_data.raise_for_status()
    except Exception:
        raise RuntimeError(errors('104'))
    formatted_data = json.loads(raw_data.text)
    if formatted_data['Response'] == 'Error':
        raise RuntimeError(errors('101', [convert]))
    return formatted_data


def get_all_coins_by_symbol(convert='USD'):
    convert = convert.upper().strip()
    if convert not in VALID_CONVERSION_CURRENCIES:
        raise ValueError(errors('101', [convert]))
    coins_data = pull_coins_data(convert)
    coins_by_symbol = {}
    duplicated_symbols = {}
    for coin in coins_data:
        symbol = coin['symbol'].lower()
        if symbol in coins_by_symbol:
            if symbol in duplicated_symbols:
                duplicated_symbols[symbol] += 1
            else:
                duplicated_symbols[symbol] = 2
            symbol = symbol+str(duplicated_symbols[symbol])
        coins_by_symbol[symbol.lower()] = coin
    return coins_by_symbol


def get_all_coins_by_name(convert='USD'):
    convert = convert.upper().strip()
    if convert not in VALID_CONVERSION_CURRENCIES:
        raise ValueError(errors('101', [convert]))
    coins_data = pull_coins_data(convert)
    coins_by_name = {}
    duplicated_names = {}
    for coin in coins_data:
        name = coin['name'].lower()
        if name in coins_by_name:
            if name in duplicated_names:
                duplicated_names[name] += 1
            else:
                duplicated_names[name] = 2
            name = name+str(duplicated_names[name])
        coins_by_name[name.lower()] = coin
    return coins_by_name


def prettify(data, convert):
    convert = convert.lower().strip()
    for coin in data:
        if convert != 'usd':
            del data[coin]['price_usd']
            del data[coin]['market_cap_usd']
            del data[coin]['24h_volume_usd']
        data[coin]['price'] = data[coin][f'price_{convert}']
        data[coin]['market_cap'] = data[coin][f'market_cap_{convert}']
        data[coin]['24h_volume'] = data[coin][f'24h_volume_{convert}']
        del data[coin][f'price_{convert}']
        del data[coin][f'market_cap_{convert}']
        del data[coin][f'24h_volume_{convert}']
    for coin in data:
        del data[coin]['id']
        for info in data[coin]:
            if info not in ['name', 'symbol', 'rank']:
                try:
                    data[coin][info] = float(data[coin][info])
                except TypeError:
                    data[coin][info] = None
            elif info == 'rank':
                data[coin][info] = int(data[coin][info])
            if info == 'last_updated':
                try:
                    data[coin][info] = datetime.datetime.fromtimestamp(
                        data[coin][info])
                except TypeError:
                    data[coin][info] = None
    return data


def get_coins(coins=[], convert='USD'):
    if isinstance(coins, str):
        if coins == '':
            list_of_coins = []
        else:
            list_of_coins = [coins.lower().strip()]
    else:
        list_of_coins = [x.lower().strip() for x in coins]
    convert = convert.upper().strip()
    coins_by_symbol = get_all_coins_by_symbol(convert)
    if len(list_of_coins) == 0:
        list_of_coins = [x for x in coins_by_symbol]
    else:
        coins_by_name = get_all_coins_by_name(convert)
    coins = {}
    for coin in list_of_coins:
        if coin in coins_by_symbol:
            coins[coin] = coins_by_symbol[coin]
        elif coin in coins_by_name:
            coins[coin] = coins_by_name[coin]
        else:
            raise KeyError(errors('103', [coin]))
    coins = prettify(coins, convert)
    if len(coins) == 1:
        for coin in coins:
            coins = coins[coin]
    return coins


def get_global_data(convert='USD'):
    global_data = pull_global_data(convert)
    convert = convert.upper().strip()
    if convert not in VALID_CONVERSION_CURRENCIES:
        raise ValueError(errors('101', [convert]))
    convert = convert.lower().strip()
    # Changes "bitcoin_percentage_of_market_cap" to "btc_dominance"
    global_data['btc_dominance'] = global_data[('bitcoin_percentage'
                                                + '_of_market_cap')]
    del global_data['bitcoin_percentage_of_market_cap']
    # Converts "last_updated" to datetime object
    try:
        global_data['last_updated'] = datetime.datetime.fromtimestamp(
            float(global_data['last_updated']))
    except TypeError:
        global_data['last_updated'] = None
    # Changes "total_market_cap_{convert}" and "total_24h_volume_{convert}"
    # to "market_cap" and "24h_volume"
    global_data['market_cap'] = global_data[f'total_market_cap_{convert}']
    global_data['24h_volume'] = global_data[f'total_24h_volume_{convert}']
    del global_data['total_market_cap_usd']
    del global_data['total_24h_volume_usd']
    return global_data


def get_historical_data(coin, convert='USD', start=None, end=None):
    convert = convert.upper().strip()
    if convert not in VALID_CONVERSION_CURRENCIES:
        raise ValueError(errors('101', [convert]))
    full_data = pull_historical_data(coin, convert)
    try:
        if start is not None:
            start_epoch = start.timestamp()
        if end is not None:
            end_epoch = end.timestamp()
    except Exception:
        raise ValueError(errors('105'))
    historical_data = []
    for data in full_data['Data']:
        if start is not None:
            if data['time'] < start_epoch:
                continue
        if end is not None:
            if data['time'] > end_epoch:
                break
        if [data['close'], data['high'], data['low']] == [0, 0, 0]:
            continue
        data['time'] = datetime.datetime.fromtimestamp(data['time'])
        historical_data.append(data)
    return historical_data


def get_news():
    return News()
