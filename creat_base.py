# в качестве примера используется orm - SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, event, ForeignKey, func,desc, extract, ForeignKeyConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

# engine - пул соединений к БД
engine = create_engine('sqlite:///test_sales.db', echo=True) # пример с sqlite
#engine = create_engine('postgresql://user:pass@192.168.1.77:5432/mydatabase') # пример с postgre

# declarative_base - фабричная функция, возвращающая базовый класс, от которого произойдет наследование класса с моделью.
Base = declarative_base()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Класс, описывающий одну из таблиц БД. Такой класс назывется моделью.

class Store(Base):          # магазины торговой сети
    __tablename__ = 'store' # имя таблицы

    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор магазина")
    address = Column(String(50), comment="адрес магазина")

    def __repr__(self):
        return "[id={0}, address={1}]".format(
            self.id,
            self.address)


class Item(Base):        # товарные позиции (уникальные наименования)
    __tablename__ = 'item' # имя таблицы

    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор товара")
    name = Column(String(50), nullable=False, unique=True, comment="наименование товара")
    price = Column(Float, nullable=False, comment="цена товара")

    def __repr__(self):
        return "[id={0}, name={1}, price={2}]".format(
            self.id,
            self.name,
            self.price)


class Sales(Base):        #   продажи
    __tablename__ = 'sales' # имя таблицы

    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор операции")
    sale_time = Column(DateTime, nullable=False, default=datetime.now(), comment="время продажи")
    item_id = Column(Integer, nullable=False, comment="Идентификатор товара")
    store_id = Column(Integer, nullable=False, comment="Идентификатор магазина")

    __table_args__ = (
        ForeignKeyConstraint(['item_id'], ["item.id"]),
        ForeignKeyConstraint(['store_id'], ["store.id"]),
    )

    def __repr__(self):
        return "[id={0}, sale_time={1}, item_id={2}, store_id={3}]".format(
            self.id,
            self.sale_time,
            self.item_id,
            self.store_id)


# создание таблиц если они не существуют
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

session.query(Sales).delete()              # удаление Store
session.commit()

session.query(Item).delete()              # удаление Store
session.commit()

session.query(Store).delete()              # удаление Store
session.commit()


for i in range(1, 21):                  # заполнение Store
    new_store = Store(address = "г. Город, ул. Городская, д. " + str(i))
    session.add(new_store)
session.commit()


for i in range(1, 31):                         # заполнение Item
    new_item = Item(name="Goods_" + str(i),
                    price=100 + i)
    session.add(new_item)
session.commit()


a = timedelta(days=31)                            # заполнение Sales

for t in [datetime.now(), datetime.now()+a]:
    for i in range(10, 31):
        new_item = Sales(item_id=i,
                         store_id=4,
                         sale_time=t)
        session.add(new_item)

    for i in range(25, 31):
        new_item = Sales(item_id=i,
                         store_id=3,
                         sale_time=t)
        session.add(new_item)

    for i in range(0, 11):
        new_item = Sales(item_id=15,
                         store_id=10,
                         sale_time=t)
        session.add(new_item)

    for i in range(0, 2):
        new_item = Sales(item_id=12,
                         store_id=11,
                         sale_time=t)
        session.add(new_item)

    for i in range(1, 3):
        for j in range(1, 3):
            new_item = Sales(item_id=i,
                             store_id=j,
                             sale_time=t)
            session.add(new_item)

session.commit()


new_item = Sales(item_id=1,
                 store_id=100)
try:
    session.add(new_item)
    session.commit()
except Exception as E:
    session.rollback()
    print("****************************************************")
    print(E)


session.close()
