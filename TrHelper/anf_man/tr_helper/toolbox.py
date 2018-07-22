import datetime
import requests
from collections import namedtuple
from django.core.cache import cache
from bs4 import BeautifulSoup
from Levenshtein import distance, jaro_winkler
from .c.app_config import config_url
from .models import LANGUAGE_CHOICES, Article, ArticleCase, Logger, TestLog
import numpy as np
import PIL
from PIL import Image
from io import BytesIO

def mse(x, y):
    return np.linalg.norm(x - y)/100

CacheArticle = namedtuple('CacheArticle', ['img_array', 'url_title', 'language'])


class NewArticle():
    '''Parse all data to Article model by url and for comparison of articles'''

    def __init__(self, url=None, soup=None, compare=False):
        self.url = url
        self.soup = soup or BeautifulSoup(
                                requests.get(url).text,
                                'lxml')
        NewArticle.compare_parse(self) if compare else NewArticle.parse(self)

    def parse(self):
        text = self.soup.select('div.entry-content')[0].get_text().strip()
        self.title = self.soup.select('h2.entry-title')[0].get_text().strip()
        self.lead = self.soup.select('p.entry-lead')[0].get_text().strip()
        self.symbols_amount = sum(map(len, [text, self.title, self.lead]))
        NewArticle.compare_parse(self)

    def compare_parse(self):
        print('parse article')
        self.url_title = self.url.split('/')[-1]

        self.img_url = self.soup.article.select('img.img-responsive')[0].get('src')
        response = requests.get(self.img_url)
        x = Image.open(
            BytesIO(response.content)
            ).resize(
            (32, 32), PIL.Image.ANTIALIAS
            ).convert('LA')
        self.img_array = np.array(x)

        for num, i in LANGUAGE_CHOICES:
            if 'anf'+i in self.url:
                self.language = i

    def __str__(self):
        return self.url_title


class Manager(NewArticle):

    def __init__(self,
            log='tr_helper/last_article_log.txt',
            url=None, soup=None):
        print(url)
        print('in init')
        NewArticle.__init__(self, url, soup)
        self.log = log
        self.logger = Logger()
        self.logger.save()

    def get_status(self, user_req=False, test=False):
        print('get status')
        print('hr')#new article to investigate
        with open(self.log) as log:
            print('hrr')
            # if test:
            #     for i in log.readlines():
            #         i, url = i.split(' ')
            #         soup = BeautifulSoup(open(i.strip()), 'lxml')
            #         comp_article = NewArticle(url=url, soup=soup, compare=True)
            for url in log.readlines()[::-1][1:]:
                print('hrrr', url)
                comp_article = cache.get(url)
                print(comp_article)
                if not comp_article:
                    print('set cache')
                    comp_article = NewArticle(url, compare=True)
                    array = comp_article.img_array
                    title = comp_article.url_title
                    lang = comp_article.language
                    val = CacheArticle(array, title, lang)
                    cache.set(url, val, 86400)

                print('got article')
                img_index = mse(self.img_array, comp_article.img_array)
                text_index = jaro_winkler(
                    self.url_title,
                    comp_article.url_title,
                    0.25
                    ) #urls is nornalized!!!
                text_2 = distance(
                    self.url_title,
                    comp_article.url_title,
                    )
                print('mse=', img_index, 'text=', text_index)
                testlog = TestLog(
                    article=comp_article.url_title,
                    img_index=img_index,
                    text_index=text_index,
                    text_2=text_2,
                    comp_article = self.logger
                    )
                 #test case for comp_article with each already added article
                print('hrrrr')
                if img_index < 15:
                    print('hrrrrr')
                    if comp_article.language != self.language:
                        query = Article.objects.get(url=url.strip())
                        print('query -- ', query)
                        if user_req:
                            testlog.decision = '2'
                            testlog.save()
                            return query

                        testlog.decision = '3'
                        testlog.save()
                        self.case = query.case

                        return 'found version'

                    if text_index == 1:
                        self.update_url = url.strip()
                        testlog.decision = '1'
                        testlog.save()
                        return 'update'

            testlog.decision = '0'
            testlog.save()
            self.case = ArticleCase()
            self.case.save()
            print('new')
            return 'new'


    def update(self):
        try:
            query = Article.objects.get(url=self.update_url)
            query.url = self.url
            query.title = self.title
            query.symbols_amount = self.symbols_amount
            query.save()
            self.logger.article = query
            self.logger.save()
        except:
            pass


    def write_bd(self):
        print('write_bd')

        new = Article(
            case = self.case,
            url=self.url,
            title=self.title,
            symbols_amount=self.symbols_amount,
            language=self.language,
            img_url=self.img_url
            )
        new.save()
        print('written')
        self.logger.article = new
        self.logger.save()



    def manage(self, user_req=False):
        print('in manager')
        if Manager.get_status(self, user_req=user_req) == 'new':
            print('in manager - new')
            Manager.write_bd(self)
        Manager.update(self)


class FlowListener():


    def __init__(self,
                url=config_url,
                # soup=None,
                log='tr_helper/last_article_log.txt'):
        self.log = log
        self.url = url
        self.last = open('tr_helper/last_article_log.txt').readlines()[-1].strip()
        # self.soup = soup or BeautifulSoup(requests.get(url).text, 'lxml')



    def start(self):
        self.soup = BeautifulSoup(requests.get(self.url).text, 'lxml')
        links = self.soup.table.find_all('a')
        urls = []
        # test_tracker = []
        for link in links:
            urls.append(link.get('href').strip())
        #
        try:
            print(self.last, urls[:5])
            print(self.last in urls[:5])
            print('pum0')
            num = urls.index(self.last)
            print('pum1')
            if num:

                print('pum3')
                url = urls[:num][-1]
                print(url)

                with open(self.log, 'a') as log:
                    log.write(url+'\n')
                Manager(url=url).manage()
                print('pum5')
        except ValueError:
            pass
