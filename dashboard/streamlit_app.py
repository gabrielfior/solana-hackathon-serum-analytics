from io import BytesIO

import streamlit as st

st.set_page_config(layout="wide")
from dotenv import load_dotenv

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
    return get_bid_ask_spread_data(orders, market_names, 0.9)


@st.experimental_memo(suppress_st_warning=True, ttl=120)
def get_orders_cache():
    conn = init_connection()
    return get_orders(conn)


orders = get_orders_cache()

selected_market_names = st.multiselect(
    'Select markets to plot',
    (orders.market_name.unique().tolist()))

d = plot_bid_asks(orders, selected_market_names, 21000)

#########################

### plotting
median_price = get_median_price(orders, selected_market_names)
#price = 21000
fig = plt.figure(figsize=(16, 9))
make_plot(fig, selected_market_names, d, median_price)
# st.pyplot(fig)

plt.tight_layout()
# plt.show()

# workaround to control fig size
buf = BytesIO()
plt.savefig(buf, format="png")
st.subheader('Order book aggregated width')
st.image(buf, width=1200)

##### plot orders
col1, col2 = st.columns(2)
orders_to_display = orders[orders.market_name.isin(selected_market_names)]
print(f'med {median_price}')

with col1:
    st.subheader('Bids')
    st.dataframe(orders_to_display[orders_to_display.is_buy == True].sort_values('price',
                                                                                 ascending=False))
with col2:
    st.subheader('Asks')
    st.dataframe(orders_to_display[orders_to_display.is_buy == False].sort_values('price',
                                                                                  ascending=True))
