from collections import deque
from bs4 import BeautifulSoup
import requests
from ..models import Article #!
#from rest_framework.renderers import JSONRenderer
import numpy as np
import PIL
from PIL import Image


class NewArticle():
    '''Parse all data to Article model by url and for comparison of articles'''

    def __init__(self, url):
        self.url = url
        NewArticle.parse(self)

    def parse(self):
        self.soup = BeautifulSoup(
            requests.get(self.url).text,
            'lxml'
            )

        lst = [
            (self.text, 'div.entry-content'),
            (self.title, 'h2.entry-title'),
            (self.lead, 'p.entry-lead'),
            (self.auth, 'li.writer'),
            (self.place, 'li.map-marker')
        ]
        for name, tag_cls in lst:
            name = self.soup.select(tag_cls)[0].get_text().strip()

        self.img_url = self.soup.find_all('img', class='img-responsive').get('scr')

        self.symbols_amount = sum(map(len, [self.text, self.title, self.lead]))


class FlowListener():

    def __init__(self, last, url=config_url):
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')
        self.last = last


    def start(self):
        '''1.exctract all links
        2. get list of urls
        3. check if last article is not last (has no zero index)
            (ищем полное совпадение url)
        4.1 if bigger then zero - we treat articles in slice
            from zero to last article index as new
        4.1.1 check every for duplication in case of updation
            (image+tag-words/ +symbols), write res to log
        4.1.1.1 if ok - write to bd, raise event "new!"
        4.1.1.2 update bd, raise event "update!"

        4.2 if error - look for previous last article
        4.2.1 if found - exctract slice and
            check for similarity with last article (4.1.1)
        4.2.2 make a regression: look for previouse-previouse and so on
            to find start point '''

        links = self.soup.table.find_all('a')
        titles = []
        for link in links:
            titles.append(link.get('href'))
        try:
            num = titles.index(self.last)
            if num:
                self.last[0] = titles[0]
                open('tr_helper/last_article_log.txt', 'a').write(self.last[0]+'\n')
                if is_new():
                    for i in links[:num]:
                        a = NewArticle(self.last)
                        # articles_queue.append(JSONRenderer().render(a.__dict__()))
                        b = Article(
                            url=a.url,
                            title=a.title,
                            symbols_amount=a.symbols_amount,
                            )
                        b.save()
        except IndexError:
            pass

def img_compare_mse(img_1, img_2):
    x = Image.open(img_1).resize((32, 32), PIL.Image.ANTIALIAS).convert('LA')
    x = np.array(x)
    y = Image.open(img_2).resize((32, 32), PIL.Image.ANTIALIAS).convert('LA')
    y = np.array(y)
    return np.linalg.norm(x - y)


check = {
    'img' : img_compare_mse,
    'title' : exctract,
    'symbols' : count,
    'tag' : tag_compare #rubr, author, place
}
res = {
    'same' : update,
    'similar' : check['something else'],
    'diffrent' : new
}
