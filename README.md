# HW_1
webapp FastAPI with SQLAlchemy Async ORM <p>
Pycharm 2021.3.3  Python 3.6<p>
Точка входа: main.py<p>
Запуск проекта: uvicorn main:app --reload , запускается на 8080 порту.<p>
Приложена тестовая база sqlite  test_sales.db, таблицы с тестовыми данными.<p>
Приложение creat_base.py для заполнения таблиц базы тестовыми данными. Запускается при необходимости вручную.<p>
Запрос 127.0.0.1:8080/stores/ ответ json json {"id": x, "address": "x"}<p>
Запрос 127.0.0.1:8080/items/ ответ json {"id": x, "name": "x", "price" : x }<p>
Запрос 127.0.0.1:8080/stores/top/ ответ json {"store_id": x, "store_address": "x", "sum_sale" : x } топ-10 магазинов по выручке за текущий месяц<p>
Запрос 127.0.0.1:8080/items/top/ ответ json {"item_id": x, "item_name": x, "item_amount" : x} топ-10 товаров по количеству продаж за текущий месяц<p>
Запрос 127.0.0.1:8080/sales/  post json {'store_id':x,'item_id':x}  ввод в таблицу продажи, ответ {'ok': True} или {'alarm': текст исключения}<p>
При post запросе обрабатывается исключение ForeignKeyConstraint на id items и id stores.<p>

