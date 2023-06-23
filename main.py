import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import create_tables, delete_tables, Publisher, Book, Shop, Stock, Sale
import json


load_dotenv()


DSN = os.getenv('DSN')
engine = sqlalchemy.create_engine(DSN)


def add_from_file():
    with open('insert_data.json', 'r') as fd:
        data = json.load(fd)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    return print('Таблицы заполнены')


def select_sale():
    arg = str(input('Введите идентификатор или наименование издательства: '))
    query = session.query(Publisher, Book, Stock, Shop, Sale)\
        .join(Book, Book.id_publisher == Publisher.id)\
        .join(Stock, Stock.id_book == Book.id).join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id_stock == Stock.id)
    if arg.isnumeric():
        records = query.filter(Publisher.id == arg).all()
    else:
        records = query.filter(Publisher.name == arg).all()
    for b in records:
        t, n, p, d = b.Book.title, b.Shop.name, b.Sale.price, b.Sale.date_sale.strftime("%d-%m-%Y")
        print("%-40s %10s %10d %15s" % (t, n, p, d))
        # print(f'{b.Book.title} | {b.Shop.name} | {b.Sale.price} | {(b.Sale.date_sale).strftime("%d-%m-%Y")}')


Session = sessionmaker(bind=engine)

with Session() as session:
    # delete_tables(engine)
    # create_tables(engine)
    # add_from_file()
    select_sale()
