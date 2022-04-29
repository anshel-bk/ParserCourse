import csv
import requests
from bs4 import BeautifulSoup


def create_csv_rows():
    with open('all_data_by_rows.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена',
                         'Ссылка на карточку'])


def make_soup(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_links_on_all():
    full_links_on_products = []
    for i in range(1, 6):
        for j in range(1, 5):
            url = f"http://stepik-parsing.ru/html/index{i}_page_{j}.html"
            soup = make_soup(url)
            link_on_products = [link.find('a', href=True)['href'] for link in soup.find_all(class_='sale_button')]
            for link in link_on_products:
                full_links_on_products.append(link)
    return full_links_on_products


def get_data_about_all_categories(url):
    soup = make_soup(url)
    print(url) #отладочный для отслеживания итерации
    name = soup.find("p", id="p_header").text
    article = soup.find("p", class_="article").text.split(":")[1].lstrip()
    brand = soup.find(id="brand").text.split(":")[1].lstrip()
    model = soup.find(id="model").text.split(":")[1].lstrip()
    stock = soup.find(id="in_stock").text.split(":")[1].lstrip()
    price = soup.find(id="price").text.split()[0].lstrip()
    old_price = soup.find(id="old_price").text.split()[0].lstrip()
    data = [name, article,brand,model,stock,price,old_price]
    data.append(url)
    return data


def write_data_csv(data):
    with open('all_data_by_rows.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)


def main():
    create_csv_rows()
    links = get_links_on_all()
    for link in links:
        url = f"http://stepik-parsing.ru/html/{link}"
        data = get_data_about_all_categories(url)
        write_data_csv(data)
    print("Информация в базу данных успешно записана")

main()



