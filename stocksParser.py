from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(
    service=Service(
        executable_path="C:\\Users\\Jury Stolyarov\\Desktop\\Тактактак\\GitHub\\ПарсингСайта\\Парсер "
                        "Акций\\chromedriver.exe"))

url = 'https://invest.yandex.ru/catalog/stock/'
response = requests.get(url)
src = response.text
soup = BeautifulSoup(src, 'lxml')

try:
    driver.get(url=url)
    SCROLL_PAUSE_TIME = 0.5

    # Получаем высоту скролла
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Скроллим вниз страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ждем загрузки страницы
        time.sleep(SCROLL_PAUSE_TIME)

        # Вычисляем новую высоту скролла и сравниваем с предыдущим
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    # Собираем всю HTML разметку после скролла в main_page
    main_page = driver.page_source
    # Создаем объект BS4 и ищем по фильтрам нужные блоки с данными.
    soup = BeautifulSoup(main_page, "lxml")
    whole_table = soup.find('div', class_='qBUYt_fIDhDD5CCxOhoS') # блок со всеми акциями
    blocks_of_stocks = whole_table.find_all('a',
                                            class_='lBT6RuJRjtvzChEJ_G30 yDtbhftw9A4mXqH3vPkH ZPgoa_UnfWgowwkvsp64 '
                                                   'N9w__d8iYPl6C0KewYiA') # отдельный блок по каждой акции
    start = 0
    # В отдельном блоке по каждой акции, ищем блоки с именем, аббревиатурой и ценой за 1 лот
    for i in blocks_of_stocks:
        stockName = i.find('div', class_='tJYWSxg23zNUv79hPvVS').text.strip()
        stockAbbreviation = i.find('div', class_='J_AA_RdDMupXrcOA53MT').text.strip()
        stockCost = i.find('div', class_='JwI6J0zVLy2AeTvQKsy2 EfpJt47uYIzH5wN4EwzV').text.strip()
        start += 1
        print(f'{start}: {stockName} ({stockAbbreviation}) цена за лот {stockCost}')

    time.sleep(1)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
