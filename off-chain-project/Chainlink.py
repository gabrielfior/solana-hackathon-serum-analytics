from chainlink_feeds.chainlink_feeds import ChainlinkFeeds
import matplotlib.pyplot as plt
import pandas as pd

cf = ChainlinkFeeds(output_format='pandas')
data = cf.get_daily_candle(pair='eth/usd')
data['closePrice'] = data['closePrice'].astype(float)
data.index = pd.to_datetime(data.index, unit='s')

print(data['closePrice'])
