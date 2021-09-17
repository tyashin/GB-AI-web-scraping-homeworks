'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB 
и реализовать функцию, записывающую собранные вакансии в созданную БД.

'''

from pymongo import MongoClient

from scrapers.hh_scraper import search_hh
from scrapers.superjob_scraper import search_superjob


def save_vacancies_to_db(vac_search_str, max_pages):

    client = MongoClient('127.0.0.1', 27017)
    jobs_db = client['jobs']
    vacs_collection = jobs_db.vacancies
    vac_data = []
    vac_data.extend(search_hh(vac_search_str, max_pages))
    vac_data.extend(search_superjob(vac_search_str, max_pages))
    vacs_collection.insert_many(vac_data)


vac_search_str = input('Подстрока в наименовании вакансии: ')
max_pages = int(input('Максимальное количество страниц с вакансиями: '))
save_vacancies_to_db(vac_search_str, max_pages)
