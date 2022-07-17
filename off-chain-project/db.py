from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker as sessionmaker
from sympy import integer_nthroot


# connect with data base
engine = create_engine("", echo=True)
# manage tables
base = declarative_base()


class Pricing(base):

    __tablename__ = "Pricing"

    # List of the columns
    pricing_id = Column(String, primary_key=True)
    date = Column(String)
    price = Column(Integer)
    price_confidence = Column(Integer)

    def __init__(self, pricing_id, date, price, price_confidence):
        self.pricing_id = pricing_id
        self.date = date
        self.price = price
        self.price_confidence = price_confidence


base.metadata.create_all(engine)
