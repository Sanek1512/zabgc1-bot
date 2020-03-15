# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

#   <-- Парсинг данных с сайта -->

URL = 'http://zabgc.ru/ras.php'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0', 'accept': 'text/css,*/*;q=0.1'}
HOST = 'http://zabgc.ru'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('ul', class_='dow_list').find_all('li')
    
    timetable = []

    for item in items:
        timetable.append({
            'title': item.find('b').get_text(strip=True),
            'download_link': HOST + item.find('a').get('href'),
            'view_link': item.find('a', target="_blank").get('href')
        })
    return timetable
    
def Parse():
    html = get_html(URL)
    if html.status_code == 200:
        timetable = get_content(html.text)
        return timetable
    else:
        print('Сайт переделали. П*ц.')