from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Float


Base = declarative_base()
class Macys(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(String)
    price_sale = Column(String)
    percent = Column(String)
    category = Column(String)
    color = Column(String)
    all_color = Column(String)
    size = Column(String)
    details = Column(String)
    images = Column(String)
    url = Column(String)

    def __init__(self, product_name, price, price_sale, percent, category, color, all_color, size, details, images, url):
        self.product_name = product_name
        self.price = price
        self.price_sale = price_sale
        self.percent = percent
        self.category = category
        self.color = color
        self.all_color = all_color
        self.size = size
        self.details = details
        self.images = images
        self.url = url

    def __repr__(self):
        return "CData '%s'" % (self.url)


class MacysPrice(Base):
    __tablename__ = "price_product"
    id = Column(Integer, primary_key=True)
    price = Column(String)
    price_sale = Column(String)
    url = Column(String)

    def __init__(self, price, price_sale, url):
        self.price = price
        self.price_sale = price_sale
        self.url = url

    def __repr__(self):
        return "CData '%s'" % (self.url)

class MacysTommy(Base):
    __tablename__ = "product_tommy"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(String)
    price_sale = Column(String)
    percent = Column(String)
    category = Column(String)
    color = Column(String)
    all_color = Column(String)
    size = Column(String)
    details = Column(String)
    images = Column(String)
    url = Column(String)

    def __init__(self, product_name, price, price_sale, percent, category, color, all_color, size, details, images, url):
        self.product_name = product_name
        self.price = price
        self.price_sale = price_sale
        self.percent = percent
        self.category = category
        self.color = color
        self.all_color = all_color
        self.size = size
        self.details = details
        self.images = images
        self.url = url

    def __repr__(self):
        return "CData '%s'" % (self.url)


class MacysPriceTommy(Base):
    __tablename__ = "price_product_tommy"
    id = Column(Integer, primary_key=True)
    price = Column(String)
    price_sale = Column(String)
    url = Column(String)

    def __init__(self, price, price_sale, url):
        self.price = price
        self.price_sale = price_sale
        self.url = url

    def __repr__(self):
        return "CData '%s'" % (self.url)


db_engine = create_engine("sqlite:///macys.db", echo=True)
Base.metadata.create_all(db_engine)
