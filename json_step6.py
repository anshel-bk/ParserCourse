import requests
from bs4 import BeautifulSoup
import json


def make_soup(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_links_by_category():
    full_links_on_products = []
    for i in range(1, 6):
        for j in range(1, 5):
            url = f"http://stepik-parsing.ru/html/index{i}_page_{j}.html"
            soup = make_soup(url)
            link_on_products = [link.find('a', href=True)['href'] for link in soup.find_all(class_='sale_button')]
            for link in link_on_products:
                full_links_on_products.append(link)
    return full_links_on_products


def get_data(url):
    soup = make_soup(url)
    categories = url.split("/")[4]
    name = soup.find('p', id='p_header').text
    article = soup.find("p", class_="article").text
    description = soup.find('ul', id='description').find_all('li')
    list_tags = [li['id'] for li in description]
    list_values = [li.text for li in description]
    price = [x.text for x in soup.find_all('p', class_='price')]
    stock = soup.find(id="in_stock").text.split(":")[1].lstrip()
    price = soup.find(id="price").text.split()[0].lstrip()
    old_price = soup.find(id="old_price").text.split()[0].lstrip()
    result_json = []
    result_json.append({
        "categories": categories,
        "name": name,
        "article": article,
        "description": {list_tags[i]: list_values[i].split(":")[1].strip() for i, value in enumerate(list_values)},
        "count": stock,
        "price": price,
        "old_price": price,
        "url": url
    },

    )

    return result_json


def write_in_json(result_json):
    with open('full_data_by_all_categories.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)


def main():
    full_categories = []
    links = get_links_by_category()
    for link in links:
        url = f"http://stepik-parsing.ru/html/{link}"
        result_json = get_data(url)
        for prod in result_json:  # цикл создается чтобы был только один список в противном случае некорректный
            full_categories.append(prod)
    write_in_json(full_categories)
    print("Запись завершена успешно")


main()

