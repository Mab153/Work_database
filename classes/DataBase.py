from json_db_lite import JSONDatabase
import os
from typing import Callable
import datetime
import functools

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

    @logging
    def add_user(self, data:User) -> None:
        """Добавление пользователя в базу данных в файл users.json"""
        try:
            id = self.__users.get_all_records()[-1]["id"] + 1
        except (IndexError, KeyError, AttributeError):
            id = 0

        except Exception as e:
            raise Exception(f"Произошла непредвиденная ошибка: {e}")

        self.__users.add_records({**{"id": id}, **data.to_dict()})
        print(f"Пользователь {data.name} добавлен")

class User:
    """Создание пользователя"""
    def __init__(self, name:str, email:str, phone_number:str):
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def to_dict(self) -> dict:
        """Получение данных пользователя в виде dictionary объекта"""
        return {"name": self.name,
                "email": self.email,
                "phone_number": self.phone_number}


if __name__ == "__main__":
    db = DataBase("My_database")

    bob = User(name='Bob', email="example@gmail.com", phone_number="123456789")

    print(bob.to_dict())

    db.add_user(bob)