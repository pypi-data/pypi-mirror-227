from ccxtools.binance import Binance


class BinanceUsdt(Binance):

    def __init__(self, who, env_vars):
        super().__init__(who, env_vars, {
            'options': {
                'defaultType': 'future',
                'fetchMarkets': ['linear']
            }
        })
        self.contract_sizes = self.get_contract_sizes()

    def get_mark_price(self, ticker):
        return float(self.ccxt_inst.fapiPublicGetPremiumIndex({'symbol': f'{ticker}USDT'})['markPrice'])

    def get_best_book_price(self, ticker, side):
        best_book_price_data = self.ccxt_inst.fapiPublicGetDepth({'symbol': f'{ticker}USDT'})[f'{side}s'][0]
        return float(best_book_price_data[0])

    def get_contract_size(self, ticker):
        return self.contract_sizes[ticker]

    def get_contract_sizes(self):
        """
        :return: {
            'BTC': 0.1,
            'ETH': 0.01,
            ...
        }
        """
        contracts = self.ccxt_inst.fetch_markets()

        sizes = {}
        for contract in contracts:
            if contract['info']['contractType'] != 'PERPETUAL' or contract['info']['marginAsset'] != 'USDT':
                continue
            if contract['info']['status'] != 'TRADING':
                continue

            ticker = contract['base']
            for fil in contract['info']['filters']:
                if fil['filterType'] == 'LOT_SIZE':
                    size = float(fil['stepSize'])

            sizes[ticker] = size

        return sizes

    def get_max_trading_qtys(self):
        """
        :return: {
            'BTC': 120,
            'ETH': 2000,
            ...
        """
        qtys = {}
        for contract in self.ccxt_inst.fetch_markets():
            if contract['linear'] and contract['quote'] == 'USDT' and contract['info']['contractType'] == 'PERPETUAL':
                ticker = contract['info']['baseAsset']
                max_qty = list(filter(lambda x: x['filterType'] == 'MARKET_LOT_SIZE', contract['info']['filters']))[0][
                    'maxQty']

                qtys[ticker] = float(max_qty)

        return qtys

    def get_max_position_qtys(self):
        """
        :return: {
            'BTC': 20000000,
            'ETH': 5000000,
            ...
        }
        """
        positions = self.ccxt_inst.fetch_positions()

        qtys = {}
        for position in positions:
            symbol = position['symbol']
            if '/' in symbol and symbol[-4:] == 'USDT':
                ticker = symbol[:symbol.find('/')]
                qtys[ticker] = int(position['info']['maxNotionalValue'])

        return qtys

    def get_balance(self, ticker):
        return super().get_balance(ticker)

    def get_position(self, ticker):
        return float(self.ccxt_inst.fapiprivatev2_get_positionrisk({'symbol': f'{ticker}USDT'})[0]['positionAmt'])

    def post_market_order(self, ticker, side, open_close, amount):
        """
        :param ticker: <String>
        :param side: <Enum: "buy" | "sell">
        :param open_close: <Enum: "open" | "close">
        :param amount: <Float | Int>
        :return: <Float> average filled price
        """
        if open_close == 'open':
            extra_params = {}
        elif open_close == 'close':
            extra_params = {'reduceOnly': 'true'}

        trade_info = self.ccxt_inst.create_market_order(f'{ticker}USDT', side, amount, params=extra_params)
        return trade_info['average']
