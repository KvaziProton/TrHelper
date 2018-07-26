import datetime
import requests
from collections import namedtuple
from django.core.cache import cache
from bs4 import BeautifulSoup
from Levenshtein import distance, jaro_winkler
from .c.app_config import config_url
from .models import LANGUAGE_CHOICES, Article, ArticleCase
import PIL
from PIL import Image
from io import BytesIO
import numpy as np

def mse(x, y):
    return np.linalg.norm(x - y)/100

CacheArticle = namedtuple('CacheArticle', ['img_array', 'url_title', 'language'])


class NewArticle():
    '''Parse all data to Article model by url and for comparison of articles'''

    def __init__(self, url=None, soup=None, compare=False):
        print('init comp_article: ', url)
        self.url = url
        self.soup = soup or BeautifulSoup(
                                requests.get(url).text,
                                'lxml')
        NewArticle.compare_parse(self) if compare else NewArticle.parse(self)

    def parse(self):
        self.text = self.soup.select('div.entry-content')[0].get_text().strip()
        self.title = self.soup.select('h2.entry-title')[0].get_text().strip()
        self.lead = self.soup.select('p.entry-lead')[0].get_text().strip()
        self.symbols_amount = sum(map(len, [self.text, self.title, self.lead]))
        # NewArticle.compare_parse(self)

    def compare_parse(self):
        print('parse article')
        self.url_title = self.url.split('/')[-1]
        try:
            self.img_url = self.soup.article.select('img.img-responsive')[0].get('src')
        except AtributeError:
            print('article is deleted')
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
            other_log = 'tr_helper/other_language_log.txt',
            decisions = 'tr_helper/decisions.txt',
            url=None, soup=None):
        NewArticle.__init__(self, url, soup)
        self.log = log
        self.other_log = other_log
        self.decisions = decisions

    def is_new(self, user_req=False, test=False):
        with open(self.log) as log, open(self.other_log) as other_log, open(self.decisions, 'a') as decisions:
            decisions.write('Compare case: '+self.url+'\n'+self.img_url+'\n')
            for url in other_log.readlines()+log.readlines()[::-1]:

                comp_article = cache.get(url.strip())
                if not comp_article:
                    print('set cache')
                    comp_article = NewArticle(url=url.strip(), compare=True)
                    array = comp_article.img_array
                    title = comp_article.url_title
                    lang = comp_article.language
                    val = CacheArticle(array, title, lang)
                    cache.set(url, val, 86400)

                img_index = mse(self.img_array, comp_article.img_array)
                text_index = jaro_winkler(
                    self.url_title,
                    comp_article.url_title,
                    0.25
                    )
                line = url+ comp_article.img_url+'\n'+ \
                'mse='+str(img_index)+', '+'text'+str(text_index)+'\n'+'\n'
                decisions.write(line)

                if img_index < 25: #denends from order
                    if comp_article.language != self.language:
                        decisions.write('found fersion'+'\n'+'\n')
                        self.similar_url = comp_article.url
                        return False

                    if text_index == 1:
                        self.update_url = comp_article.url
                        decisions.write('update'+'\n'+'\n')
                        return False

            decisions.write('write to bd'+'\n'+'\n')
        if user_req:
            with open(self.other_log, 'a') as other_log:
                other_log.write(url+'\n')

        print('new')
        return True

    def update(self):
        print('in update')
        query = Article.objects.get(url=self.update_url)
        query.url = self.url
        query.title = self.title
        query.symbols_amount = self.symbols_amount
        query.save()

    def write_bd(self):
        print('write_bd')
        self.case = ArticleCase()
        self.case.save()
        new = Article(
            case = self.case,
            url=self.url,
            title=self.title,
            symbols_amount=self.symbols_amount,
            language=self.language,
            img_url=self.img_url
            )
        new.save()



    def manage(self):
        print('in manager')
        if Manager.is_new(self):

            print('in manager - new')
            Manager.write_bd(self)
            return
        else:
            Manager.update(self)
            return


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
                Manager(url=url).manage()
                with open(self.log, 'a') as log:
                    log.write(url+'\n')

                print('pum5')
        except ValueError:
            pass
