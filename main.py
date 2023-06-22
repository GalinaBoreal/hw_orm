import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker, joinedload
import json
from dotenv import load_dotenv

load_dotenv()

from models import create_tables, delete_tables, Publisher, Book, Shop, Stock, Sale

DSN = os.getenv('DSN')
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
# delete_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()


def add_from_file(file):
    with open(file, 'r') as fd:
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

# add_from_file('insert_data.json')

query = session.query(Book).join(Book.publisher).filter(Publisher.id == 1).all()
print(query)
