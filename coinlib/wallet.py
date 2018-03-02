import coinlib


class Wallet():

    def __init__(self, content={}):
        coins_by_symbol = coinlib.get_all_coins_by_symbol()
        coins_by_name = coinlib.get_all_coins_by_name()
        self.content = {}
        for coin in content:
            coin_lower = coin.lower().strip()
            if (coin_lower not in coins_by_symbol
                and coin_lower not in coins_by_name):
                raise ValueError(coinlib.errors('103', [coin]))
            else:
                self.content[coin_lower] = content[coin]

    def get_value(self, convert='USD'):
        if len(self.content) == 0:
            return 0
        convert = convert.upper().strip()
        if convert not in coinlib.VALID_CONVERSION_CURRENCIES:
            raise ValueError(coinlib.errors('101', [convert]))
        content_coins = coinlib.get_coins(list(self.content.keys()), convert)
        values = []
        for coin in content_coins:
            values.append(content_coins[coin]['price']*self.content[coin])
        return sum(values)

    def add(self, coin, quantity):
        coin = coin.lower().strip()
        if coin in self.content:
            self.content[coin] += quantity
        else:
            self.content[coin] = quantity
        return self.content

    def add_many(self, coins):
        for coin in coins:
            coin = coin.lower().strip()
            if coin in self.content:
                self.content[coin] += coins[coin]
            else:
                self.content[coin] = coins[coin]
        return self.content

    def subtract(self, coin, quantity):
        self.content[coin.lower().strip()] -= quantity
        return self.content

    def subtract_many(self, coins):
        for coin in coins:
            coin = coin.lower().strip()
            self.content[coin] -= coins[coin]
        return self.content

    def remove(self, coin):
        del self.content[coin.lower().strip()]
        return self.content

    def remove_many(self, coins):
        for coin in coins:
            coin = coin.lower().strip()
            del self.content[coin]
