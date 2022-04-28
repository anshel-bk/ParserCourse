import csv

import requests
from random import choice

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def create_csv_rows():
    with open('all_data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')



def get_data_csv(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    names = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.split('\n') for x in soup.find_all('div', class_='description')]
    price = [x.text for x in soup.find_all('p', class_='price')]
    results = []
    for name, description, price in zip(names, description, price):
        result = []
        flatten = name, [desc.split(":")[1].strip() for desc in description if desc], price
        for x in flatten:
            if isinstance(x, list):
                for i in x:
                    result.append(i)
            else:
                result.append(x)
        results.append(result)
    return results


def write_data_csv(data):
    with open('all_data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)


def fill_table():
    create_csv_rows()
    for i in range(1, 6):
        for j in range(1, 5):
            url = f"http://stepik-parsing.ru/html/index{i}_page_{j}.html"
            data = get_data_csv(url)
            for dat in data:
                write_data_csv(dat)
    print("Таблица полностью заполнена")


fill_table()
