import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
import datetime as dt

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    __tableargs__ = {'comment': 'Издательство'}

    id = sq.Column(sq.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.id} {self.name}'


class Book(Base):
    __tablename__ = "book"
    __tableargs__ = {'comment': 'Книга'}

    id = sq.Column(sq.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = sq.Column(sq.String(length=40), nullable=False, unique=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id', ondelete='CASCADE'))

    publisher = relationship('Publisher', backref='Book')

    def __repr__(self):
        return f'{self.id} {self.title} {self.id_publisher}'


class Shop(Base):
    __tablename__ = "shop"
    __tableargs__ = {'comment': 'Магазин'}

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    name = sq.Column(sq.String(length=40), unique=True)

    def __repr__(self):
        return f'{self.id} {self.name}'


class Stock(Base):
    __tablename__ = "stock"
    __tableargs__ = {'comment': 'Ассортимент'}

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id', ondelete='CASCADE'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id', ondelete='CASCADE'))
    count = sq.Column(sq.Integer, comment='Количество книг')

    book = relationship('Book', backref='stock')
    shop = relationship('Shop', backref='stock')

    def __repr__(self):
        return f'{self.id} {self.id_book} {self.id_shop} {self.count}'


class Sale(Base):
    __tablename__ = "sale"
    __tableargs__ = {'comment': 'Продажи'}

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    price = sq.Column(sq.NUMERIC, nullable=False, )
    date_sale = sq.Column(sq.DateTime, default=dt.datetime.utcnow)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id', ondelete='CASCADE'))
    count = sq.Column(sq.Integer, comment='Проданное количество книг')

    stock = relationship('Stock', backref='sale')

    def __repr__(self):
        return f'{self.id} {self.price} {self.date_sale} {self.id_stock}, {self.count}'


def create_tables(engine):
    Base.metadata.create_all(engine)
    return print('Таблицы созданы')


def delete_tables(engine):
    Base.metadata.drop_all(engine)
    return print('Таблицы удалены')
