import pandas as pd
from matplotlib import pyplot as plt


def get_orders(conn):
    orders = pd.read_sql_table('orders', conn)
    orders = orders[orders.fetched_at_epoch == orders.fetched_at_epoch.max()]
    orders['volume'] = orders['price'] * orders['size']
    return orders

def get_median_price(orders, market_names):
    orders_to_display = orders[orders.market_name.isin(market_names)]
    median_price = (orders_to_display[orders_to_display.is_buy == True].sort_values('price', ascending=False).iloc[
                        0].price +
                    orders_to_display[orders_to_display.is_buy == False].sort_values('price', ascending=True).iloc[
                        0].price) / 2
    return median_price

def get_bid_ask_spread_data(orders, market_names, percentile=0.95) -> dict:
    d = {}
    for market_name in market_names:
        btc_orders = orders[(orders.market_name == market_name)]

        if len(btc_orders) == 0:
            raise Exception('no data')

        buys = btc_orders[btc_orders['is_buy'] == True].sort_values('price', ascending=False)
        sales = btc_orders[btc_orders['is_buy'] == False].sort_values('price', ascending=True)

        if percentile is not None:
            buys = buys[buys.price > buys.price.quantile(1 - percentile)]
            sales = sales[sales.price < sales.price.quantile(percentile)]

        cumsum_buys = buys['volume'].cumsum()
        cumsum_sales = sales['volume'].cumsum()
        d[market_name] = {
            'buys_x': buys['price'],
            'buys_y': cumsum_buys,
            'sales_x': sales['price'],
            'sales_y': cumsum_sales
        }
    return d


def make_plot(fig, market_names, d, price):
    ax = fig.add_subplot(111)
    for market_name in market_names:
        ax.plot(d[market_name]['buys_x'], d[market_name]['buys_y'], 'o-', label=f'Bid - {market_name}',
                drawstyle="steps", linewidth=2)
        ax.plot(d[market_name]['sales_x'], d[market_name]['sales_y'], 'o-', label=f'Bid - {market_name}',
                drawstyle="steps", linewidth=2)

    ax.legend(loc='lower right')
    ax.axvline(price, linewidth=1, color='gray')
    ax.set_xlabel('Price (USD)')
    ax.set_ylabel('Volume (USD)')
    return fig
