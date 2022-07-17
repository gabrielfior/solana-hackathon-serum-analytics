import streamlit as st
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from utils import *

load_dotenv()
import os
from sqlalchemy import create_engine


st.title('Serum Analytics Dashboard')

@st.experimental_singleton
def init_connection():
    engine = create_engine(os.environ['db_url'])
    return engine.connect()

@st.cache(suppress_st_warning=True, ttl=120)
def plot_bid_asks(orders, market_names, price):
    return plot_bid_ask_spread(orders, market_names, price)

@st.experimental_memo(suppress_st_warning=True, ttl=120)
def get_orders_cache():
    conn = init_connection()
    return get_orders(conn)




market_names = ['BTC/USDC', 'BTC/USDT']

orders = get_orders_cache()

selected_market_names = st.multiselect(
     'Select markets to plot',
     (market_names))

d = plot_bid_asks(orders, market_names, 21000)


### plotting
price = 21000

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
for market_name in selected_market_names:
    ax.plot(d[market_name]['buys_x'],d[market_name]['buys_y'], '-', label=f'Bid - {market_name}', drawstyle="steps", linewidth=2)
    ax.plot(d[market_name]['sales_x'],d[market_name]['sales_y'], '-', label=f'Bid - {market_name}', drawstyle="steps", linewidth=2)

plt.axvline(price, linestyle='--', linewidth=1., color='gray')
plt.legend(loc='lower right')
ax.set_xlabel('Price (USD)')
ax.set_ylabel('Volume (USD)')
st.pyplot(fig)
