from bs4 import BeautifulSoup
import requests
from .c.app_config import config_url
from Levenshtein import distance, jaro_winkler
from .func import mse
import datetime
from .models import LANGUAGE_CHOICES, Article, ArticleCase, Logger, TestLog



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
        for num, i in LANGUAGE_CHOICES:
            if 'anf'+i in self.url:
                self.language = i

    def __str__(self):
        return self.url_title


        # rubr = self.soup.select('h2.section-title title')[1].get_text().split()[2:]
        #
        # items = self.title + '\n' + self.lead
        # spesial = '\xe2'+'\x80'+ '\x9c' +'\x99' --- если выделять из url, то уже нормализованы
        # for i in string.punctuation+special:
        #     items.replace(i, ' ')
        # items = items.split()
        #
        # other = [i
        #     for i in items
        #     if i.isnumeric() or i[0].isupper()]
        #


class Manager(NewArticle):

    def __init__(self,
            log='tr_helper/last_article_log.txt',
            url=None, soup=None):
        print(url)
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
                comp_article = NewArticle(url, compare=True)
                print('got article')
                img_index = mse(self.img_url, comp_article.img_url)
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
                if not img_index:
                    print('hrrrrr')
                    if comp_article.language != self.language:
                        testlog.decision = '3'
                        query = Article.objects.get(url=url.strip())
                        if user_req:
                            testlog.decision = '2'
                            testlog.save()
                            return self.query

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



    def manage(self):
        print('in manager')
        if Manager.get_status(self) == 'new':
            print('in manager - new')

            Manager.write_bd(self)

            return
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

                with open(self.log, 'a') as log:
                    log.write(url+'\n')
                Manager(url=url).manage()
                print('pum5')
        except ValueError:
            pass
