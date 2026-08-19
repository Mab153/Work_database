# 📦 JSON Database Manager

Универсальная библиотека для работы с JSON-базами данных с автоматическим логированием и поддержкой CRUD операций.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

## 📋 Описание

**JSON Database Manager** — это легковесная ORM-подобная обертка для работы с JSON-хранилищами. Проект создан для автоматизации учета смен в пунктах выдачи заказов (ПВЗ Ozon), но может использоваться в любых проектах, где требуется простое и надежное хранение данных в JSON.

### 🎯 Основные возможности

- ✅ **Автоматическая генерация ID** — уникальные идентификаторы для каждой записи
- ✅ **Встроенное логирование** — все операции записываются в `logs.json` с timestamp
- ✅ **Простой API** — интуитивно понятные методы для работы с данными
- ✅ **Инкапсуляция** — скрытая работа с файловой системой
- ✅ **Расширяемость** — легкое добавление новых сущностей

### 🗂️ Структура данных
My_database/
├── users.json # Пользователи системы
├── works.json # Работы/смены
├── schedules.json # Расписания
└── logs.json # История операций

Базовое использование
from DataBase import DataBase, User

# Создание экземпляра базы данных
db = DataBase("My_database")

# Создание пользователя
user = User(
    name="Иван Петров",
    email="ivan@mail.com",
    phone_number="+79991234567"
)

# Добавление пользователя
db.add_user(user)
# Вывод: Пользователь Иван Петров добавлен

Пример работы с логами
# Все операции автоматически логируются
db.add_user(user1)  # Запись в logs.json
db.add_user(user2)  # Запись в logs.json

# Структура лога:
{
    "operation_type": "add_user",
    "date": "2026-08-19 15:30:45.123456",
    "data": {
        "args": [{"name": "Иван", "email": "ivan@mail.com", ...}]
    }
}
