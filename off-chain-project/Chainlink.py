from chainlink_feeds.chainlink_feeds import ChainlinkFeeds
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import plotly.graph_objs as go


# pip install chainlink-feeds
# pip install websockets


# Chainlink subgraph
cf = ChainlinkFeeds(output_format='pandas')

# Data returned by the subgraph
data = cf.get_hourly_candle(pair='eth/usd')
data.index = pd.to_datetime(data.index, unit='s')


# Converting data to float
data['closePrice'] = data['closePrice'].astype(float)
data['averagePrice'] = data['averagePrice'].astype(float)
data['openPrice'] = data['openPrice'].astype(float)
data['lowPrice'] = data['lowPrice'].astype(float)
data['highPrice'] = data['highPrice'].astype(float)

# Plotting
# declare figure
fig = go.Figure()

# Candlestick

fig.add_trace(go.Candlestick(x=data.index,
                             open=data['openPrice'],
                             high=data['highPrice'],
                             low=data['lowPrice'],
                             close=data['closePrice'],
                             name='marketData'
                             ))

# Add titles

fig.update_layout(
    title='Chainlink live price eth/usd',
    yaxis_title='price of eth/usdc'
)

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")

        ])
    )
)

# Show
fig.show()
