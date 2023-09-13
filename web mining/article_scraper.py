from database import Article, create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup

# database function
def opendb():
    engine = create_engine('sqlite:///example.db')
    Session = sessionmaker(bind=engine)
    return Session()

def save(article):
    db = opendb()
    db.add(article)
    db.commit()
    db.close()
    print("Article saved.")

def get_soup():
    url = 'https://blog.jetbrains.com'
    try:
        page = requests.get(url)
        if page.status_code == 200:
            print('Success!')
            return BeautifulSoup(page.text, 'html.parser')
        elif page.status_code == 404:
            print('Page Not Found.')
        elif page.status_code == 503:
            print('Service Unavailable.')
    except Exception as e:
        print('Error', e)

def extract(soup):
    target = soup.find('div', class_ = 'latest')
    if not target:
        print("target area found")
        return
    articles = target.find_all('div', class_='col')
    if not articles:
        print("articles not found")
        return
    total = len(articles)
    print("articles found")
    print("Total articles found: ", total)
    for item in articles:
        try: pubdate = item.find('time')['datetime']
        except: pubdate = None
        title = item.find('h3').text
        summary = item.find('p').text
        author = item.find('span').text
        img_src = item.find('img')['src']
        article = Article(
            title=title,
            pubdate=pubdate,
            summary=summary,
            author=author,
            imgsrc=img_src
        )
        save(article)

if __name__ == "__main__":
    soup = get_soup()
    try:
        extract(soup)
        print("Done.")
    except Exception as e:
        print("Could not get data", e)