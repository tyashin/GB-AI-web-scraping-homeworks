
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import requests


def search_superjob(vacancy, max_pages):
    vac_list = []
    page_counter = 1

    params = {
        'keywords': vacancy,
        'profession_only': 1,
        'page': 1
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }

    url = 'https://superjob.ru/vacancy/search/'

    while page_counter <= max_pages:
        response = requests.get(url, params=params, headers=headers)

        if not response.ok:
            return vac_list

        dom = bs(response.text, 'html.parser')
        vacancy_divs = dom.find_all(
            'div', {'class': 'f-test-search-result-item'})

        for vac_div in vacancy_divs:
            vac_data = {}
            vac_data['site'] = 'superjob.ru'

            vac_name = vac_div.find(
                'div', {'class': 'jNMYr GPKTZ _1tH7S'})

            vac_data['name'] = None
            if vac_name:
                vac_a = vac_name.find('a')
                if vac_a:
                    if vac_a['href']:
                        vac_data['url'] = 'https://superjob.ru' + vac_a['href']

                    vac_data['name'] = vac_a.getText()

            if vac_data['name'] is None:
                continue

            vac_employer = vac_div.find(
                'span', {'class': 'f-test-text-vacancy-item-company-name'})

            if vac_employer:
                vac_vac_employer_a = vac_employer.find('a')

                if vac_vac_employer_a:
                    vac_data['employer'] = vac_vac_employer_a.getText()

            vac_loc = vac_div.find(
                'span', {'class': 'f-test-text-company-item-location'})

            if vac_loc:
                vac_loc_list = vac_loc.findChildren()
                if len(vac_loc_list) == 3:
                    vac_data['location'] = vac_loc_list[2].getText()

            vac_data_salary = vac_div.find(
                'span', {'class': 'f-test-text-company-item-salary'})
            if vac_data_salary:
                salary_string = vac_data_salary.getText()
                vac_data['salary_string'] = salary_string
                split_string = salary_string.split('\xa0')
                vac_data['currency'] = ''

                if salary_string.find('от') != -1:
                    vac_data['salary_from'] = int(
                        split_string[1] + split_string[2])
                    vac_data['currency'] = split_string[3].replace('.', '')
                elif (salary_string.find('до') != -1) and (len(split_string) >= 3):
                    vac_data['salary_to'] = int(
                        split_string[1] + split_string[2])
                    vac_data['currency'] = split_string[3].replace('.', '')
                elif len(split_string) == 3:
                    vac_data['salary_from'] = int(
                        split_string[0] + split_string[1])
                    vac_data['currency'] = split_string[2].replace('.', '')
                elif len(split_string) >= 6:
                    vac_data['salary_from'] = int(
                        split_string[0] + split_string[1])
                    vac_data['salary_to'] = int(
                        split_string[3] + split_string[4])
                    vac_data['currency'] = split_string[5].replace('.', '')

                vac_data['currency'] = vac_data['currency'].replace(
                    "руб/месяц", "руб")
                vac_data['currency'] = float(
                    'nan') if vac_data['currency'] == '' else vac_data['currency']

            vac_list.append(vac_data)

        page_counter += 1
        if page_counter <= max_pages:
            next_page_a = dom.find(
                'a', {'class': 'f-test-button-keyboard_arrow_right'})

            if next_page_a:
                params['page'] = page_counter
            else:
                break

    return vac_list
