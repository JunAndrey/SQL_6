import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()
class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(length=40), nullable=False)

    def __str__(self):
        return f'Publisher {self.id}: {self.name})'

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.VARCHAR(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"))

    publisher = relationship(Publisher, backref="book")
    def __str__(self):
        return f'Book {self.id}: ({self.title}, {self.id_publisher})'

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(length=40), nullable=False)

    def __str__(self):
        return f'Shop {self.id}: {self.name})'



class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    count = sq.Column(sq.Integer, nullable=False)

    shop = relationship(Shop, backref="stock")
    book = relationship(Book, backref="stock")



    def __str__(self):
        return f'Stock {self.id}: ({self.id_shop}, {self.id_book}, {self.count})'

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))

    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f'Sale {self.id}: ({self.price}, {self.date_sale}, {self.count}, {self.id_stock})'



def create_table(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)