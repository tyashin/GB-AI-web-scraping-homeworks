'''
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:

    название источника;
    наименование новости;
    ссылку на новость;
    дата публикации.
    [дайджест каждой новости]

'''
import json
from datetime import datetime, timedelta
from pprint import pprint

import newspaper
import nltk
import requests
from lxml import html


def augment_news_item(news_item):

    try:
        article = newspaper.Article(
            url=news_item['url'], language='ru')
        article.download()
        article.parse()
        article.nlp()
        news_item['summary'] = article.summary.replace('\n', ' ')

        if article.publish_date:
            news_item['publish_date'] = article.publish_date.strftime(
                '%d/%m/%Y')

    except:
        pass

    return news_item


def scrape_lenta_ru():

    news_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    url = 'https://lenta.ru'
    response = requests.get(url, headers=headers)

    if not response.ok:
        return news_list

    dom = html.fromstring(response.text)
    items = dom.xpath("//div[@class='b-yellow-box__wrap']/div[@class='item']")

    for item in items:
        news_item = {}
        news_item['source_name'] = 'lenta.ru'
        news_item['title'] = (
            ' '.join(item.xpath("./a/text()"))).strip().replace('\xa0', ' ')

        news_item_path = (item.xpath("./a/@href")[0]).strip()
        news_item['url'] = ''
        news_item['summary'] = ''
        news_item['publish_date'] = ''

        if news_item_path:
            news_item['url'] = url + (item.xpath("./a/@href")[0]).strip()
            news_item = augment_news_item(news_item)

        news_list.append(news_item)

    return news_list


def scrape_yandex_news():

    news_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    url = 'https://yandex.ru/news'
    response = requests.get(url, headers=headers)

    if not response.ok:
        return news_list

    dom = html.fromstring(response.text)
    items = dom.xpath("//article")

    for item in items:
        news_item = {}
        news_item['source_name'] = " ".join(item.xpath(
            ".//span[@class='mg-card-source__source']//a/text()")).replace('\xa0', ' ')

        news_item['title'] = " ".join(item.xpath(
            ".//div[@class='mg-card__text']//h2/text()")).replace('\xa0', ' ').strip()

        if not news_item['title']:
            continue

        news_item_path = item.xpath(
            ".//span[@class='mg-card-source__source']//a/@href")

        if news_item_path:
            news_item['url'] = news_item_path[0].strip()

        news_item['summary'] = " ".join(item.xpath(
            ".//div[@class='mg-card__annotation']/text()")).replace('\xa0', ' ')

        p_date = (item.xpath(
            ".//span[@class='mg-card-source__time']/text()")[0]).strip()

        if len(p_date) == 5:
            p_date = datetime.now().strftime('%d/%m/%Y')

        elif p_date.lower().find('вчера'):
            p_date = (datetime.now() - timedelta(1)).strftime('%d/%m/%Y')
        else:
            p_date = ''

        news_item['publish_date'] = p_date

        news_list.append(news_item)

    return news_list


def scrape_news_mail_ru():

    news_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    url = 'https://news.mail.ru'
    response = requests.get(url, headers=headers)

    if not response.ok:
        return news_list

    dom = html.fromstring(response.text)
    hrefs = dom.xpath(
        "//a[@class='newsitem__title link-holder']/@href | //a[@class='link link_flex']/@href")

    for href in hrefs:

        href = href.strip()

        if not href:
            continue

        response_1 = requests.get(href, headers=headers)

        if not response_1.ok:
            continue

        dom_1 = html.fromstring(response_1.text)
        news_item = {}

        try:
            news_item['title'] = (dom_1.xpath(
                "//h1/text()")[0]).replace('\xa0', ' ').strip()
        except:
            continue

        try:
            news_item['source_name'] = (dom_1.xpath(
                "//a[@class='link color_gray breadcrumbs__link']/span/text()")[0]).replace('\xa0', ' ').strip()
        except:
            continue

        news_item['url'] = href

        try:
            news_item['summary'] = (dom_1.xpath(
                "//div[contains(@class, 'article__intro')]/p/text()")[0]).replace('\xa0', ' ').strip()
        except:
            news_item['summary'] = ''

        try:
            date_str = dom_1.xpath(
                "//span[@class = 'note__text breadcrumbs__text js-ago']/@datetime")[0]

            news_item['publish_date'] = date_str[8:10] + \
                '/' + date_str[5:7] + '/' + date_str[:4]
        except:
            news_item['publish_date'] = ''

        news_list.append(news_item)

    return news_list


# Используем NLP для получения дайджеста статьи (для lenta.ru, просто по приколу)
nltk.download('punkt')

news_data = []
news_data.extend(scrape_lenta_ru())
news_data.extend(scrape_yandex_news())
news_data.extend(scrape_news_mail_ru())
pprint(news_data)

with open('news.json', 'w', encoding='utf8') as f:
    json.dump(news_data, f, ensure_ascii=False)
