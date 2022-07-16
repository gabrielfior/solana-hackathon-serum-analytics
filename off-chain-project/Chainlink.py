from chainlink_feeds.chainlink_feeds import ChainlinkFeeds
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd


# Chainlink subgraph.
cf = ChainlinkFeeds(output_format='pandas')

# Data returned by the subgraph
data = cf.get_hourly_candle()
data.index = pd.to_datetime(data.index, unit='s')


data['closePrice'] = data['closePrice'].astype(float)
data['averagePrice'] = data['averagePrice'].astype(float)
data['openPrice'] = data['openPrice'].astype(float)
