from celery import shared_task
from collections import deque
from bs4 import BeautifulSoup
import requests
from .models import Article

articles_queue = deque()
site_url = 'https://anfenglish.com/latest-news'
#from witch start search (if selery will fall - after restart we can start from fail moment)
#but we should store it somewhere - in logging file, may be (or in bd?)
last_article = [open('tr_helper/last_article_log.txt').readlines()[-1].strip(),]
print(last_article)

class NewArticle():
    '''Parse all data to Article model by url and text to downloarding'''

    def __init__(self, url):
        self.url = url
        NewArticle.parse(self)

    def parse(self):
        self.soup = BeautifulSoup(
            requests.get(self.url).text,
            'lxml'
            )
        #text attr - is a list of strings
        text = self.soup.find('article').get_text().splitlines()
        #clean from empty elemensts and symbols of '\t'
        self.text = [line.strip('\t') for line in text if line]
        #first element is a title of the article
        self.title = self.text[0]
        #don't forget to delete superfluous info
        self.symbols_amount = sum([len(line) for line in self.text])


#only best case for now
@shared_task
def check_if_new(last_article=last_article, soup=BeautifulSoup(requests.get(site_url).text, 'lxml')):
    #get list of articles by title
    titles = []
    links = soup.table.find_all('a')
    for link in links:
        titles.append(link.get_text().strip())
        #because if editor apdate article - last number in url will be changed
        #so we check titles
    num = titles.index(last_article[0])

    if num:
        last_article[0] = titles[0]
        open('tr_helper/last_article_log.txt', 'a').write(last_article[0])
        for i in links[:num]:
            a = NewArticle(i.get('href'))
            articles_queue.append(a)
            b = Article(
                url=a.url,
                title=a.title,
                symbols_amount=a.symbols_amount,
                )
            b.save()

    return last_article
