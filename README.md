# HW_1
webapp FastAPI with SQLAlchemy Async ORM
Pycharm 2021.3.3  Python 3.6
����� �����: main.py
������ �������: uvicorn main:app --reload , ����������� �� 8080 �����.
��������� �������� ���� sqlite  test_sales.db, ������� � ��������� �������.
���������� creat_base.py ��� ���������� ������ ���� ��������� �������. ����������� ��� ������������� �������.
������ 127.0.0.1:8080/stores/ ����� json json {"id": x, "address": "x"}
������ 127.0.0.1:8080/items/ ����� json {"id": x, "name": "x", "price" : x }
������ 127.0.0.1:8080/stores/top/ ����� json {"store_id": x, "store_address": "x", "sum_sale" : x } ���-10 ��������� �� ������� �� ������� �����
������ 127.0.0.1:8080/items/top/ ����� json {"item_id": x, "item_name": x, "item_amount" : x} ���-10 ������� �� ���������� ������ �� ������� �����
������ 127.0.0.1:8080/sales/  post json {'store_id':x,'item_id':x}  ���� � ������� �������, ����� {'ok': True} ��� {'alarm': ����� ����������}
��� post ������� �������������� ���������� ForeignKeyConstraint �� id items � id stores.

