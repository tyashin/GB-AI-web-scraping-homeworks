
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import requests


def search_hh(vacancy, max_pages):
    vac_list = []
    page_counter = 0

    params = {
        'text': vacancy,
        'search_field': 'name',
        'page': 0
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }

    url = 'https://hh.ru/search/vacancy'

    while page_counter <= max_pages:
        response = requests.get(url, params=params, headers=headers)

        if not response.ok:
            return vac_list

        dom = bs(response.text, 'html.parser')
        vacancy_divs = dom.find_all(
            'div', {'class': 'vacancy-serp-item'})

        for vac_div in vacancy_divs:
            vac_data = {}
            vac_data['site'] = 'hh.ru'
            vac_data_a = vac_div.find(
                'a', {'data-qa': 'vacancy-serp__vacancy-title'})

            vac_data['name'] = None

            if vac_data_a:
                vac_data['name'] = vac_data_a.getText()

                vac_data_url = vac_data_a['href']
                vac_data['url'] = urljoin(
                    vac_data_url, urlparse(vac_data_url).path)

            if vac_data['name'] is None:
                continue

            vac_data_employer = vac_div.find(
                'a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            if vac_data_employer:
                vac_data['employer'] = vac_data_employer.getText()

            vac_data_location = vac_div.find(
                'span', {'data-qa': 'vacancy-serp__vacancy-address'})
            if vac_data_location:
                vac_data['location'] = vac_data_location.getText()

            vac_data_salary = vac_div.find(
                'span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vac_data_salary:
                salary_string = vac_data_salary.getText()
                vac_data['salary_string'] = salary_string
                split_string = salary_string.replace('\u202f', '').split(' ')

                if salary_string.find('от') != -1:
                    vac_data['salary_from'] = int(split_string[1])
                    vac_data['currency'] = split_string[2].replace('.', '')
                elif salary_string.find('до') != -1:
                    vac_data['salary_to'] = int(split_string[1])
                    vac_data['currency'] = split_string[2].replace('.', '')
                else:
                    vac_data['salary_from'] = int(split_string[0])
                    vac_data['salary_to'] = int(split_string[2])
                    vac_data['currency'] = split_string[3].replace('.', '')

            vac_list.append(vac_data)

        page_counter += 1
        if page_counter <= max_pages:
            next_page_a = dom.find('a', {'data-qa': 'pager-next'})

            if next_page_a:
                params['page'] = page_counter
            else:
                break

    return vac_list
