import csv
import requests
from bs4 import BeautifulSoup


def create_csv_rows():
    with open('all_data_by_rows.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса',
                         'Материал браслета', 'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена',
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
    data = []
    description = [info.text.split('\n') for info in soup.find_all('div', class_='description')][0]
    description = [info.strip().split(": ") for info in description if info]  # сплит сделал вместе с пробелом так как
    # в одном из сайтов производителя hdd
    # есть двоеточие в адресе из-за этого все ломается
    data = list(map(lambda info: info[1].strip() if len(info) == 2 else info[0].strip(), description))[:-1]  # последний
    # элемент, который попадает в карточку, называется купить он не нужен обрезаем
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
