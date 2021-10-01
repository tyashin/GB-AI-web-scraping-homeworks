# -*- coding: utf-8 -*-
import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse

from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'здесь логин'
    insta_pwd = 'Здесь зашифрованный пароль'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'ai_machine_learning'  # Пользователь, у которого собираем посты. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = 'eddbde960fed6bde675388aac39a3657'  # hash для получения данных по постах с главной страницы

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        yield scrapy.FormRequest(  # заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:  # Проверяем ответ после авторизации
            yield response.follow(
                # Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя
        variables = {'id': user_id,  # Формируем словарь для передачи даных в запрос
                     'first': 12}  # 12 постов. Можно больше (макс. 50)
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'  # Формируем ссылку для получения данных о постах
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        )

    def user_posts_parse(self, response: HtmlResponse, username, user_id,
                         variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')  # Сами посты
        for post in posts:  # Перебираем посты, собираем данные
            item = InstaparserItem(
                user_id=user_id,
                photo=post['node']['display_url'],
                likes=post['node']['edge_media_preview_like']['count'],
                post=post['node']
            )
        yield item  # В пайплайн

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
