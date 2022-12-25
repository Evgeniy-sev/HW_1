import asyncio
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

from pydantic import BaseModel

from sqlalchemy import select, Column, Integer, String, Float, DateTime, ForeignKeyConstraint, func, desc, extract, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = FastAPI()
engine = create_async_engine('sqlite+aiosqlite:///test_sales.db')
Base = declarative_base()


class NoteIn(BaseModel):
    store_id: int
    item_id: int


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор магазина")
    address = Column(String(50), comment="адрес магазина")

    def __repr__(self):
        return "[id={0}, address={1}]".format(
            self.id,
            self.address)


class Item(Base):        # товарные позиции (уникальные наименования)
    __tablename__ = 'item'

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


#Base.metadata.create_all(engine)

async_session = sessionmaker(bind=engine, class_=AsyncSession)
session = async_session()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")         # создание базы при старте приложения, если она отсутсвует
async def startup():
    await init_models()


@app.on_event("shutdown")         # закрытие сессии при остановке приложения
async def shutdown():
    await session.close()


@event.listens_for(Engine, "connect")                           #включение проверки foreign_keys
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@app.get('/stores/') # декорируем функцию на обслуживание get-запросов (из браузера) на путь http://127.0.0.1:8080/
async def stores():
    result = await session.execute("select * from store")

    stor_list = []
    [stor_list.append(dict(row)) for row in result]

    return JSONResponse(stor_list)  #в ответе на запрос отправляем json {"id": x, "address": "x"}


@app.get('/items/') #  путь http://127.0.0.1:8080/items/
async def items():
    result = await session.execute("select * from item")

    item_list = []
    [item_list.append(dict(row)) for row in result]

    return JSONResponse(item_list)  #в ответе на запрос отправляем json {"id": x, "name": "x", "price" : x }


@app.get('/stores/top/') #  путь http://127.0.0.1:8080/stores/top/
async def stores_top():
    query = await session.execute(select(Sales.store_id, Store.address.label('store_address'), func.sum(Item.price).label('sum_sale'))
                                  .where(extract('month', Sales.sale_time) == datetime.today().month)
                                  .join(Item, Sales.item_id == Item.id)
                                  .join(Store, Sales.store_id == Store.id)
                                  .group_by(Sales.store_id).order_by(desc('sum_sale')).limit(10))

    item_list = []
    [item_list.append(dict(row)) for row in query]

    return JSONResponse(item_list)  #в ответе на запрос отправляем json {"store_id": x, "store_address": "x", "sum_sale" : x }


@app.get('/items/top/') # путь http://127.0.0.1:8080/items/top/
async def items_top():
    query = await session.execute(select(Sales.item_id, Item.name.label('item_name'), func.count(Sales.item_id).label('item_amount'))
                                  .where(extract('month', Sales.sale_time) == datetime.today().month)
                                  .join(Item, Sales.item_id == Item.id)
                                  .group_by(Sales.item_id).order_by(desc('item_amount'))
                                  .order_by('item_id').limit(10))

    item_list = []
    [item_list.append(dict(row)) for row in query]

    return JSONResponse(item_list)  #в ответе на запрос отправляем json {"item_id": x, "item_name": x, "item_amount" : x}


@app.post('/sales/') #  путь http://127.0.0.1:8080/sales/
async def creat_note(note: NoteIn):
    try:
        query = insert(Sales).values(sale_time=datetime.now(), item_id=note.item_id, store_id=note.store_id)
        await session.execute(query)
        await session.commit()
        return JSONResponse({'ok': True})
    except Exception as E:
        await session.rollback()
        return JSONResponse({'alarm': str(E)})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

# uvicorn main:app --reload  запуск приложения

