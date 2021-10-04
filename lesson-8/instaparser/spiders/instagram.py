# -*- coding: utf-8 -*-
import configparser
import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from instaparser.items import InstaparserItem
from itertools import takewhile


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    config = configparser.ConfigParser()
    config.read("config.ini")
    insta_login = config['DEFAULT']['INSTAGRAM_LOGIN']
    insta_pwd = config['DEFAULT']['INSTAGRAM_SEC_PASSWORD']
    max_pages = int(config['DEFAULT']['MAX_PAGES']) # Не хочу ждать, пока обработается 170тыс фолловеров.
    page_count = 0

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['ai_machine_learning', 'cashcats']  # Пользователь, у которого собираем посты. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'

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
            for instauser in self.parse_user:
                yield response.follow(
                    # Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{instauser}',
                    callback=self.connections_parse,
                    cb_kwargs={'username': instauser}
                )

    def connections_parse(self, response, username):
        user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя
        variables = {'count': 12,  # Формируем словарь для передачи даных в запрос
                     'search_surface': 'follow_list_page'
                     }

        url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
        yield response.follow(url_followers,
                              headers={'User-Agent': 'Instagram 64.0.0.14.96'},
                              callback=self.body_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'connection_type': 'followers',
                                         'variables': deepcopy(variables)})

        url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}'
        yield response.follow(url_following,
                              headers={'User-Agent': 'Instagram 64.0.0.14.96'},
                              callback=self.body_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'connection_type': 'following',
                                         'variables': deepcopy(variables)})

    def body_parse(self, response, username, user_id, connection_type,
                   variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        users = j_data.get('users')
        for user in users:
            loader = ItemLoader(item=InstaparserItem(), response=response)
            loader.add_value('parent_name', username)
            loader.add_value('parent_id', user_id)
            loader.add_value('user_id', user.get('pk'))
            loader.add_value('user_name', user.get('full_name'))
            loader.add_value('user_photo', user.get('profile_pic_url'))
            loader.add_value('user_photo_file', user.get('profile_pic_url'))
            loader.add_value('image_urls', [user.get('profile_pic_url')])
            loader.add_value('connection_type', connection_type)
            yield loader.load_item()

        next_page = j_data.get('next_max_id')
        self.page_count += 1
        if next_page and self.page_count <= self.max_pages:
            variables['max_id'] = next_page
            url = f'https://i.instagram.com/api/v1/friendships/{user_id}/{connection_type}/?{urlencode(variables)}'

            yield response.follow(url,
                                  headers={'User-Agent': 'Instagram 64.0.0.14.96'},
                                  callback=self.body_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'connection_type': connection_type,
                                             'variables': deepcopy(variables)})

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
