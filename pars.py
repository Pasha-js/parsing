import requests
from bs4 import BeautifulSoup
import csv
import os


URL = 'https://auto.ria.com/uk/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'accept': '*/*' }
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars = []

    for item in items:
        ua_price = item.find('span', class_='size16')
        if ua_price:
            ua_price = ua_price.get_text()
        else:
            ua_price= 'Ціни немає'
        cars.append({
            'title': item.find('div', class_='proposition_title').get_text(strip=True),
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price': item.find('span', class_='green').get_text(),
            'ua_price': ua_price,
            'town': item.find('i', class_='i16_pin').find_previous('span').get_text(),

        })

    return cars 

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссилка', 'Ціна в долларах', 'Ціна в гривнях', 'Місто'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['ua_price'], item['town']])
        
def parse():
    URL = input('Сюди введіть ссилку на сайт')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count +1):
            print(f"Парсинг сторінки{page} из {pages_count}")
            html = get_html(URL, params={'page':page})             
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобілей')
        # os.startfile(FILE)
    else:
        print('Error')



parse()