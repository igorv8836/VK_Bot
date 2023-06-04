import requests
from bs4 import BeautifulSoup

a = "https://webservices.mirea.ru/upload/iblock/145/nm0oup23k1406umgjq00mdewalurd4f6/IIT_1-kurs_22_23_vesna_27.04.2023.xlsx"
b = "https://webservices.mirea.ru/upload/iblock/a9a/vd0ew6sbdfgjp79zz3rtetmo84wy9qxd/IIT_2-kurs_22_23_vesna_15.05.2023.xlsx"
c = "https://webservices.mirea.ru/upload/iblock/9d1/2n7qyf32jm80rk7j3gb236fj32a87eet/IIT_3-kurs_22_23_vesna_22.05.2023.xlsx"


def parse():
    page = requests.get("https://www.mirea.ru/schedule/")
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.find("div", {"class": " schedule"}). \
        find(string="Институт информационных технологий"). \
        find_parent("div"). \
        find_parent("div"). \
        findAll()  # получить ссылки
    for x in result:
        if :  # среди всех ссылок найти нужную
            f = open("file.xlsx", "wb")  # открываем файл для записи, в режиме wb
    resp = requests.get(...)  # запрос по ссылке
    f.write(resp.content)