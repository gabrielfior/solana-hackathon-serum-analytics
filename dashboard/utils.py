import pandas as pd


def get_orders(conn):
    orders = pd.read_sql_table('orders', conn)
    orders['volume'] = orders['price'] * orders['size']
    return orders


def plot_bid_ask_spread(orders, market_names, price):
    d = {}

    for market_name in market_names:
        btc_orders = orders[(orders.market_name == market_name)]

        if len(btc_orders) == 0:
            raise Exception('no data')

        buys = btc_orders[btc_orders['is_buy'] == True].sort_values('price', ascending=False)
        sales = btc_orders[btc_orders['is_buy'] == False].sort_values('price', ascending=True)

        cumsum_buys = buys['volume'].cumsum()
        cumsum_sales = sales['volume'].cumsum()
        d[market_name] = {
            'buys_x': buys['price'],
            'buys_y': cumsum_buys,
            'sales_x': sales['price'],
            'sales_y': cumsum_sales
        }
        # ax.plot(, , '-', label=f'Bid - {market_name}', drawstyle="steps", linewidth=2)
        # ax.plot(, '-', label=f'Ask - {market_name}', drawstyle="steps")
        # plt.axvline(price, linestyle='--', linewidth=1., color='gray')

    # ax.legend()
    # ax.set_xlabel('Price (USD)')
    # ax.set_ylabel('Volume (USD)')
    # print ('oi')
    # print (fig, ax)
    # return fig, ax
    return d
