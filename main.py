import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from model import create_tables, Publisher, Book, Stock, Shop, Sale
from dotenv import load_dotenv
import os.path

dotenv_path = 'config.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
login = os.getenv('login')
password_psq = os.getenv('password_psq')
database = os.getenv('database')

DSN = f"postgresql://{login}:{password_psq}@localhost:5432/{database}"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'rt') as f:
    data = json.load(f)

for line in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line.get('model')]
    session.add(model(id=line.get('pk'), **line.get('fields')))
session.commit()

def book_sale_list(search=input('Введите имя издателя или идентификатор: ')):
    search = search
    if search.isnumeric():
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Book.id_publisher == Publisher.id) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == search).all()
        for book, shop, price, date in results:
            print(f'{book} | {shop} | {price} | {date}')
        else:
            results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
                .join(Publisher, Book.id_publisher == Publisher.id) \
                .join(Stock, Stock.id_book == Book.id) \
                .join(Shop, Shop.id == Stock.id_shop) \
                .join(Sale, Sale.id_stock == Stock.id) \
                .filter(Publisher.name == search).all()
            for book, shop, price, date in results:
                print(f'{book} | {shop} | {price} | {date}')

session.close()

book_sale_list()