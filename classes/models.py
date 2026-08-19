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

class Work:
    """Создание типа работы"""
    def __init__(self, work_name:str, sallary:float):
        self.work_name = work_name
        self.salary = sallary

    def to_dict(self) -> dict:
        """Получение данных о типе работы в виде dictionary объекта"""
        return {"work_name": self.work_name,
                "salary": self.salary}

class Shift:
    def __init__(self, user_id:int, work_id:int, date:datetime.date):
        self.user_id = user_id
        self.work_id = work_id
        self.date = date

    def to_dict(self) -> dict:
        return {"user_id": self.user_id,
                "work_id": self.work_id,
                "date": self.date.strftime("%d.%m.%Y")}