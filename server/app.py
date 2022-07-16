import datetime
from fastapi import FastAPI
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import pandas as pd
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every
import pathlib

dir_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
print ('dir', dir_path)
load_dotenv(dir_path.joinpath('.env'))

database_uri = os.environ['db_url']
sessionmaker = FastAPISessionMaker(database_uri)

app = FastAPI()



@app.on_event("startup")
@repeat_every(seconds=10)  # 1 hour
def fetch_serum_order_book() -> None:
    print ('entered')
    print (datetime.datetime.now())
    with sessionmaker.context_session() as db:
        engine = db.get_bind()
        df = pd.DataFrame(dict(prices=[1],index=[1]))
        df.to_sql('dummy_table2',engine, if_exists='append')
        print ('wrote to db')