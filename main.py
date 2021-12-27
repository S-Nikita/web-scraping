import bs4
import requests

HEADERS = {'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
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

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

ret = requests.get('https://habr.com/ru/all/', headers=HEADERS)
ret.raise_for_status()
soup = bs4.BeautifulSoup(ret.text, 'html.parser')

# Получение всех статей
articles = soup.find_all('article', class_='tm-articles-list__item')
for article in articles:
    # Получение превью статей
    snippets = article.find_all('div', class_='tm-article-snippet')
    for snippet in snippets:
        # Получение хабов
        hubs = snippet.find_all('a', class_='tm-article-snippet__hubs-item-link')
        hubs = set(hub.find('span').text.lower() for hub in hubs)
        # получение отдельных элементов превью
        title = snippet.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2')
        article_preview = snippet.find('div', class_='article-formatted-body article-formatted-body_version-2')
        if article_preview and title and hubs:
            # Поиск совпадений среди всей текстовой информации превью
            if hubs & set(KEYWORDS) or any([word in title.text.lower() for word in KEYWORDS]) or any([word in article_preview.text.lower() for word in KEYWORDS]):
                # Получение необходимых параметров для вывода информации
                date = snippet.find('time')['title']
                href = snippet.find('a', class_='tm-article-snippet__readmore')['href']
                print(f'Дата: {date}; заголовок: "{title.text}"; ссылка: "https://habr.com{href}"')


