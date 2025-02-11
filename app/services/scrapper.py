import requests
from bs4 import BeautifulSoup

WEBSITES = [
    {
        "name": "espn",
        "address": "https://www.espn.com/nba/",
        "base": "https://www.espn.com",
        "selector": ".headlineStack__header + section > ul > li > a",
    },
    {
        "name": "bleacher_report",
        "address": "https://bleacherreport.com/nba",
        "base": "",
        "selector": ".articleTitle",
    },
     {
    "name": 'slam',
    "address": 'https://www.slamonline.com/',
    "base": '',
    "selector": '.h-bloglist-block-content-top > h3 > a',
  },
  {
    "name": 'yahoo',
    "address": 'https://sports.yahoo.com/nba/?guccounter=1',
    "base": 'https://sports.yahoo.com',
    "selector": '.js-content-viewer',
  },
  {
    "name": 'nba',
    "address": 'https://www.nba.com/news/category/top-stories',
    "base": 'https://www.nba.com',
    "selector": '.flex-1 > a',
  },
]

NBA_WEBSITES = [
  {
    "name": 'nba',
    "address": 'https://www.nba.com/news/category/top-stories',
    "base": 'https://www.nba.com',
    "selectorUrl": '.ArticleTile_tileMainContent__c_bU1 > a',
    "selectorTitle":
      '.ArticleTile_tileMainContent__c_bU1 > a > header > h3 > span ',
  },
  {
    "name": 'nba_canada',
    "address": 'https://www.sportingnews.com/ca/nba/news',
    "base": 'https://www.sportingnews.com',
    "selectorUrl": '.list-item__title > a',
    "selectorTitle": '.list-item__title > a',
  },
]

""" 
Web scrapper to retrieve news/articles about basketballl from different websites

Inpired by the following sources:

    https://github.com/kevinn03/nba_api

    by Kevin Nguyen

"""


# Get data from a website
def get_data(website):
    try:
        articles = []
        response = requests.get(website["address"])
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        for element in soup.select(website["selector"]):
            title = element.get_text(strip=True)
            url = element.get("href")
            if url and not url.startswith("http"):
                url = website["base"] + url
            if title:
                articles.append({"title": title, "url": url, "source": website["name"]})
        
        # Filter out empty titles
        return [article for article in articles if article["title"] != ""]
    except Exception as e:
        print(f"Error: {e}")
        return []

# Get data from NBA website
def get_nba_data(website):
    try:
        response = requests.get(website["address"])
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        nba_articles = []
        nba_title = [title.get_text(strip=True) for title in soup.select(website["selectorTitle"])]
        nba_url = [url.get("href") for url in soup.select(website["selectorUrl"])]

        for i in range(len(nba_title)):
            nba_articles.append({
                "title": nba_title[i],
                "url": website["base"] + nba_url[i],
                "source": website["name"]
            })
        
        return nba_articles
    except Exception as e:
        print(f"Error: {e}")
        return []

# Get articles from all websites
def get_articles():
    articles = []
    for website in WEBSITES:
        articles.extend(get_data(website))

    for website in NBA_WEBSITES:
        articles.extend(get_nba_data(website))

    return articles