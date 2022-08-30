import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import config
import os
from config import DSN_2
import Models_2
from Models_2 import create_table, Publisher, Book, Shop, Stock, Sale
import json

DSN = config.DSN_2
engine = sqlalchemy.create_engine(DSN)
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

log_file_name = 'contributor.json'
base_path = os.getcwd()
full_path = os.path.join(base_path, log_file_name)

with open(full_path, 'r', encoding="utf-8") as file:
    datafile = json.load(file)
    for read in datafile:
        print(read)
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
            }[read.get('model')]
        session.add(model(id=read.get('pk'), **read.get('fields')))


for d in session.query(Publisher).all():
    print(d)
pul_id_inp = input('Введите id издателя : ')


subq = session.query(Publisher).filter(Publisher.id == pul_id_inp).subquery()
for publ_shop in session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Stock.id_book == Book.id).join(subq, Book.id_publisher == subq.c.id).all():
    print(f'Издатель {pul_id_inp} продаётся в ', publ_shop)



session.commit()

session.close()
