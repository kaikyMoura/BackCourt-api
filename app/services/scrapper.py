import requests
from bs4 import BeautifulSoup

WEBSITES = [
    {
        "name": "espn",
        "address": "https://www.espn.com/nba/",
        "base": "https://www.espn.com",
        "selectorTitle": "#news-feed .contentItem .contentItem__title",
        "selectorUrl": "a.contentItem__padding",
        "selectorImage": "img"
    },
    # {
    #     "name": "bleacher_report",
    #     "address": "https://bleacherreport.com/nba",
    #     "base": "",
    #     "selector": ".articleTitle",
    #     "selectorUrl": 'img',
    #     "selectorImage": 'img'
    # },
    # {
    #     "name": 'slam',
    #     "address": 'https://www.slamonline.com/',
    #     "base": '',
    #     "selector": '.h-bloglist-block-content-top > h3 > a',
    #     "selectorUrl": 'img',
    #     "selectorImage": 'img'
    # },
]

NBA_WEBSITES = [
    {
        "name": 'nba',
        "address": 'https://www.nba.com/news/category/top-stories',
        "base": 'https://www.nba.com',
        "selectorUrl": '.ArticleTile_tileMainContent__c_bU1 > a',
        "selectorTitle": '.ArticleTile_tileMainContent__c_bU1 > a > header > h3 > span',
        "selectorImage": '.ArticleTile_tileImage__no39y img'
    },
    {
        "name": 'nba_canada',
        "address": 'https://www.sportingnews.com/ca/nba/news',
        "base": 'https://www.sportingnews.com',
        "selectorUrl": '.list-item__title > a',
        "selectorTitle": '.list-item__title > a',
        "selectorImage": '.ArticleTile_tileImage__no39y'
    },
]

""" 
Web scrapper to retrieve news/articles about basketball from different websites

Inspired by the following sources:

    https://github.com/kevinn03/nba_api

    by Kevin Nguyen

"""

# Get data from a website
def get_data(website):
    try:
        articles = []
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        })

        response = session.get(website["address"])
        if response.status_code != 200:
            print(f"Failed to retrieve data from {website['name']}, status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        titles = [title.get_text(strip=True) for title in soup.select(website["selectorTitle"])]
        urls = [url.get("href") for url in soup.select(website["selectorUrl"])]
        image_elements = soup.select(website["selectorImage"])

        for i, title in enumerate(titles):
            url = urls[i] if i < len(urls) else None
            if url and not url.startswith("http"):
                url = website["base"] + url

            image_url = None
            if i < len(image_elements):
                img_element = image_elements[i]
                if img_element:
                    image_url = img_element.get("src") or img_element.get("srcset", "").split(",")[0].split(" ")[0]
                    print(image_url)
            if title:
                articles.append({
                    "title": title,
                    "url": url,
                    "source": website["name"],
                    "image": image_url
                })

        return articles

    except Exception as e:
        print(f"Error: {e}")
        return []

# Get articles from all websites
def get_articles():
    articles = []
    for website in WEBSITES:
        articles.extend(get_data(website))

    for website in NBA_WEBSITES:
        articles.extend(get_data(website))

    return articles