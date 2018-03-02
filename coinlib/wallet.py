import coinlib


class Wallet():

    def __init__(self, contents={}):
        coins_by_symbol = coinlib.get_all_coins_by_symbol()
        coins_by_name = coinlib.get_all_coins_by_name()
        self.contents = {}
        for coin in contents:
            coin_lower = coin.lower().strip()
            if (coin_lower not in coins_by_symbol
                    and coin_lower not in coins_by_name):
                raise ValueError(coinlib.errors('103', [coin]))
            else:
                self.contents[coin_lower] = contents[coin]

    def get_value(self, convert='USD'):
        if len(self.contents) == 0:
            return 0
        convert = convert.upper().strip()
        if convert not in coinlib.VALID_CONVERSION_CURRENCIES:
            raise ValueError(coinlib.errors('101', [convert]))
        contents_coins = coinlib.get_coins(list(self.contents.keys()), convert)
        values = []
        for coin in contents_coins:
            values.append(contents_coins[coin]['price']*self.contents[coin])
        return sum(values)

    def add(self, coin, quantity):
        coin = coin.lower().strip()
        if coin in self.contents:
            self.contents[coin] += quantity
        else:
            self.contents[coin] = quantity
        return self.contents

    def add_many(self, coins):
        for coin in coins:
            coin = coin.lower().strip()
            if coin in self.contents:
                self.contents[coin] += coins[coin]
            else:
                self.contents[coin] = coins[coin]
        return self.contents

    def subtract(self, coin, quantity):
        self.contents[coin.lower().strip()] -= quantity
        return self.contents

    def subtract_many(self, coins):
        for coin in coins:
            coin = coin.lower().strip()
            self.contents[coin] -= coins[coin]
        return self.contents

    def remove(self, coin):
        del self.contents[coin.lower().strip()]
        return self.contents

    def remove_many(self, coins):
        for coin in coins:
            coin = coin.lower().strip()
            del self.contents[coin]
