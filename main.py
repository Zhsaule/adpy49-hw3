# Домашнее задание к лекции 3.«Web-scrapping»
# Попробуем получать интересующие нас статьи на хабре самыми первыми :)
# Необходимо парсить страницу со свежими статьями (https://habr.com/ru/all/) и выбирать те статьи,
# в которых встречается хотя бы одно из ключевых слов (эти слова определяем в начале скрипта).
# Поиск вести по всей доступной preview-информации (это информация, доступная непосредственно с текущей страницы).
# Вывести в консоль список подходящих статей в формате: <дата> - <заголовок> - <ссылка>.
#
# Дополнительное (необязательное) задание
# Улучшить скрипт так, чтобы он анализировал не только preview-информацию статьи, но и весь текст статьи целиком.
# Для этого потребуется получать страницы статей и искать по тексту внутри этой страницы.
import requests
import bs4

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'linux']
HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'
}
# Ваш код
base_url = 'https://habr.com'
response = requests.get(base_url, headers=HEADERS)
soup = bs4.BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all("article")

print(f'Введите условия для парсинга слов {KEYWORDS}: \n'
      f'1 - Поиск по preview-информации;\n'
      f'2 - По тексту статьи целиком.')
type_ = input()

for article in articles:
    preview = article.find(class_="tm-article-snippet")
    preview = preview.text
    if int(type_) == 2:
        post_url = base_url + article.find(class_='tm-article-snippet__title-link').attrs['href']
        resp_post = requests.get(post_url, "article", headers=HEADERS)
        soup = bs4.BeautifulSoup(resp_post.text, features='html.parser')
        post_all = soup.find("article")
        preview = preview + post_all.text
    preview = preview.replace("'s", '').lower().split()
    preview = ["".join(filter(str.isalnum, word)) for word in preview]
    if set(KEYWORDS) & set(preview):
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        link = base_url + href
        title = article.find('h2').find('span').text
        result = f'{title}\n   - {link}'
        print(result)
