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

            serialized_args = [
                a.to_dict() if hasattr(a, 'to_dict') else a 
                for a in args
            ]

            self.__logs.add_records({"operation_type": func.__name__,
                                     "date": str(datetime.datetime.now()),
                                     "data":{"args": serialized_args}})
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
    
# Работа с пользователями
    def get_all_users(self) -> list[dict]:
        return self.__users.get_all_records()

    @logging
    def add_user(self, data:User) -> None:
        """Добавление пользователя в базу данных в файл users.json"""
        id = self.__get_id(self.__users)

        self.__users.add_records({**{"id": id}, **data.to_dict()})

    @logging
    def update_user(self, user_id:int, new_data:User) -> None:
        if len(self.__users.find_records_by_key("id", user_id)) > 0:
            self.__users.update_record_by_key({"id": user_id}, new_data.to_dict())
        else:
            raise Exception("Пользователь с таким id не найден")

# Работа с типами работ
    def get_all_works(self) -> list[dict]:
        return self.__works.get_all_records()

    @logging
    def add_work(self, data:Work) -> None:
        """Добавление типа работы в базу данных в файл works.json"""
        id = self.__get_id(self.__works)

        self.__works.add_records({**{"id": id}, **data.to_dict()})

# Работа со сменами
    def get_all_shifts(self) -> list[dict]:
        return self.__schedules.get_all_records()
    
    @logging
    def add_shift(self, data:Shift):
        if (user_len := len(self.__users.find_records_by_key("id", data.user_id))) > 0 and (work_len := len(self.__works.find_records_by_key("id", data.work_id))) > 0:
            self.__schedules.add_records({"user_id": data.user_id,
                                          "work_id": data.work_id,
                                          "datetime": data.date.strftime("%d.%m.%Y")})
        elif user_len <= 0 and work_len <= 0:
            raise Exception(f'Не существуют такие пользователь и работа: {data.user_id}, {data.work_id}')
        elif user_len <= 0:
            raise Exception(f'Не существует пользователя с id {data.user_id}')
        elif work_len <= 0:
            raise Exception(f'Не существует работы с id {data.work_id}')


if __name__ == "__main__":
    db = DataBase("My_database")

    bob = User(name='Bob', email="example@gmail.com", phone_number="123456789")

    bob.name = "Bob1"

    db.update_user(0, bob)

    # db.add_user(bob)

    # giver = Work("Выдача", 3500)

    # db.add_work(giver)

    # db.add_shift(Shift(0,0,datetime.date(2026,10,5)))