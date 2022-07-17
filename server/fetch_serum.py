import dataclasses
import time

import pandas as pd
from pyserum.connection import conn
from pyserum.connection import get_live_markets
from pyserum.market import Market


@dataclasses.dataclass
class Order:
    is_buy: bool
    price: float
    size: float
    market_address: str
    market_name: str
    fetched_at_epoch: int


class SerumFetcher:
    TABLENAME = 'orders'

    def __init__(self, engine, solana_api_endpoint) -> None:
        self.fetched_at_epoch = int(time.time())
        self.engine = engine
        self.SOLANA_API_ENDPOINT = solana_api_endpoint

    def fetch_markets(self):
        markets = get_live_markets()
        return markets

    def fetch_asks_bids(self, market_address):
        # Load the given market
        cc = conn(self.SOLANA_API_ENDPOINT)
        market = Market.load(cc, market_address)
        asks = market.load_asks()
        bids = market.load_bids()
        return asks, bids

    def build_order_from_ask_bid(self, ask_or_bid, market):
        return Order(is_buy=ask_or_bid.side.name == 'BUY',
                     price=ask_or_bid.info.price,
                     size=ask_or_bid.info.size,
                     market_name=market.name,
                     market_address=market.address,
                     fetched_at_epoch=self.fetched_at_epoch)

    def build_orders(self, asks, bids, market):
        orders = []
        for ask in asks:
            order = self.build_order_from_ask_bid(ask, market)
            orders.append(order)

        for bid in bids:
            order = self.build_order_from_ask_bid(bid, market)
            orders.append(order)

        return orders

    def write_orders(self, orders, engine):
        df = pd.DataFrame(orders)
        df.to_sql(self.TABLENAME, engine, if_exists='append', index=False)

    def run(self):
        markets = self.fetch_markets()
        for market in markets:
            print(f'fetching {market}')
            asks, bids = self.fetch_asks_bids(market.address)
            new_orders = self.build_orders(asks, bids, market)
            self.write_orders(new_orders, self.engine)


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    engine = os.environ['db_url']
    solana_api_endpoint = os.environ['SOLANA_API_MAINNET']
    sf = SerumFetcher(engine, solana_api_endpoint)
    sf.run()
