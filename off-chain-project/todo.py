
import asyncio
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey, SOLANA_DEVNET_HTTP_ENDPOINT, SOLANA_DEVNET_WS_ENDPOINT


async def write_live_price_in_db():

    # devnet https://pyth.network/price-feeds/?cluster=devnet#Crypto.SOL/USD
    # PAIR : SOL/USD
    # Key : J83w4HKfqxwcq3BEMMkPFSppX3gqekLyLJBexebFVkix

    account_key = SolanaPublicKey(
        "J83w4HKfqxwcq3BEMMkPFSppX3gqekLyLJBexebFVkix")
    solana_client = SolanaClient(
        endpoint=SOLANA_DEVNET_HTTP_ENDPOINT, ws_endpoint=SOLANA_DEVNET_WS_ENDPOINT)
    price: PythPriceAccount = PythPriceAccount(account_key, solana_client)

    await price.update()

    price_status = price.aggreagate_price_status
    if price_status == PythPriceStatus.TRADING:
        # Sample output : "SOL/USD is  ... +/- ... "
        print("SOL/USD is", price.aggregate_price, "±",
              price.aggregate_price_confidence_interval)
    else:
        print("SOL/USD is not valid now. Status is", price_status)

    await solana_client.close()

asyncio.run(write_live_price_in_db())

# ToDo - Fetch live price (from Pyth) and write into DB
# sqlalchemy.create_engine(db_url)
# df.to_sql('table_name', engine, if_exists='append')


def write_historical_prices_in_db():
    # ToDo - Fetch historical prices (last 7 days) and write into DB
    # To be done only once
    pass
