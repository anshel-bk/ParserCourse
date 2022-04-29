import requests
from bs4 import BeautifulSoup
import json


def make_soup(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_links_on_phones():
    full_links_on_products = []
    for i in range(1, 5):
        url = f"http://stepik-parsing.ru/html/index1_page_{i}.html"
        soup = make_soup(url)
        link_on_products = [link.find('a', href=True)['href'] for link in soup.find_all(class_='sale_button')]
        for link in link_on_products:
            full_links_on_products.append(link)
    return full_links_on_products


def get_data(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = make_soup(url)

    name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.strip().split('\n') for x in soup.find_all('div', class_='description')]
    price = [x.text for x in soup.find_all('p', class_='price')]

    result_json = []
    for list_item, price_item, name in zip(description, price, name):
        result_json.append({
            'name': name,
            'brand': [x.split(':')[1] for x in list_item][0].lstrip(),
            'diagonal': [x.split(':')[1] for x in list_item][1].strip("\"").lstrip(),
            'material': [x.split(':')[1] for x in list_item][2].lstrip(),
            'resolution': [x.split(':')[1] for x in list_item][3].lstrip(),
            'price': price_item.split()[0]

        })
    return result_json


def write_in_json(result_json):
    with open('phones.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)



def main():
    full_categories = []
    get_links_on_phones()
    for i in range(1, 5):
        url = f"http://stepik-parsing.ru/html/index2_page_{i}.html"
        result_json = get_data(url)
        for prod in result_json:        # цикл создается чтобы был только один список в противном случае некорректный
            full_categories.append(prod)
            print(prod)
    print(full_categories)
    write_in_json(full_categories)


main()
