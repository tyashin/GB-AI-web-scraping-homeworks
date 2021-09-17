'''
2. Написать функцию, которая производит поиск и выводит на экран вакансии
с заработной платой больше введённой суммы.
'''

from pymongo import MongoClient
from pprint import pprint


def search_by_salary(min_salary):

    client = MongoClient('127.0.0.1', 27017)
    jobs_db = client['jobs']
    vacs_collection = jobs_db.vacancies

    vac_data = vacs_collection.find({'$or': [{'salary_from': {'$gt': min_salary}}, {
        'salary_to': {'$gt': min_salary}}]}, {'_id': 0})

    return vac_data


min_salary = int(input('Укажите минимальную з.п. для поиска вакансий: '))
vac_data = search_by_salary(min_salary)

for i in vac_data:
    pprint(i)
