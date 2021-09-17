'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB 
и реализовать функцию, записывающую собранные вакансии в созданную БД.

'''

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

jobs_db = client['jobs']
vacs_collection = jobs_db.vacancies


print(123)
