'''
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
'''

from pymongo import MongoClient, ASCENDING

from scrapers.hh_scraper import search_hh
from scrapers.superjob_scraper import search_superjob


def save_vacancies_to_db(vac_search_str, max_pages):

    client = MongoClient('127.0.0.1', 27017)
    jobs_db = client['jobs']
    vacs_collection = jobs_db.vacancies

    # Будем считать URL уникальным признаком, однозначно идентифицирующим вакансию.
    # Уникальный индекс по полю URL не позволит вставить другой документ с таким же значением этого поля.
    # Конечно, в продакшене индекс надо создавать вне процедуры сохранения данных, но для д.з. это приемлемо, к.м.к.
    vacs_collection.create_index([("url", ASCENDING)], unique=True)

    vac_data = []
    vac_data.extend(search_hh(vac_search_str, max_pages))
    vac_data.extend(search_superjob(vac_search_str, max_pages))

    for i in vac_data:
        try:
            vacs_collection.insert_one(i)
        except:
            pass


vac_search_str = input('Подстрока в наименовании вакансии: ')
max_pages = int(input('Максимальное количество страниц с вакансиями: '))
save_vacancies_to_db(vac_search_str, max_pages)
