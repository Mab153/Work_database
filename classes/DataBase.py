from json_db_lite import JSONDatabase
import os
from typing import Callable
import datetime
import functools
from models import User, Work, Shift

class DataBase:
    def __init__(self, name:str):
        """Создание экземпляра класса DataBase"""
        self.__name = name

        if not os.path.isdir(f"./{self.__name}"):
            os.makedirs(f"./{self.__name}", exist_ok=True)

        self.__users = JSONDatabase(os.path.join(".", self.__name, "users.json"))
        self.__works = JSONDatabase(os.path.join(".", self.__name, "works.json"))
        self.__schedules = JSONDatabase(os.path.join(".", self.__name, "schedules.json"))
        self.__logs = JSONDatabase(os.path.join(".", self.__name, "logs.json"))

    def logging(func: Callable):
        """Сбор логов в файл logs.json"""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.__logs.add_records({"operation_type": func.__name__,
                                     "date": str(datetime.datetime.now()),
                                     "data": {"args": [a.to_dict() for a in args]}})
            return result
        return wrapper

    def __get_id(self, database:JSONDatabase) -> int:
        try:
            id = database.get_all_records()[-1]["id"] + 1
        except (IndexError, KeyError, AttributeError):
            id = 0
        
        except Exception as e:
            raise Exception(f"Произошла непредвиденная ошибка: {e}")

        return id

    @logging
    def add_user(self, data:User) -> None:
        """Добавление пользователя в базу данных в файл users.json"""
        id = self.__get_id(self.__users)

        self.__users.add_records({**{"id": id}, **data.to_dict()})

    @logging
    def add_work(self, data:Work) -> None:
        """Добавление типа работы в базу данных в файл works.json"""
        id = self.__get_id(self.__works)

        self.__works.add_records({**{"id": id}, **data.to_dict()})

    @logging
    def add_shift(self, data:Shift):
        if (user_len := len(self.__users.find_records_by_key("id", data.user_id))) > 0 and (work_len := len(self.__works.find_records_by_key("id", data.work_id))) > 0:
            self.__schedules.add_records({"user_id": data.user_id,
                                          "work_id": data.work_id,
                                          "datetime": data.date.strftime("%d.%m.%Y")})
        elif user_len <= 0:
            raise Exception(f'Не существует пользователя с id {data.user_id}')
        elif work_len <= 0:
            raise Exception(f'Не существует работы с id {data.user_id}')


if __name__ == "__main__":
    db = DataBase("My_database")

    bob = User(name='Bob', email="example@gmail.com", phone_number="123456789")

    db.add_user(bob)

    giver = Work("Выдача", 3500)

    db.add_work(giver)

    db.add_shift(Shift(0,0,datetime.date(2026,10,5)))