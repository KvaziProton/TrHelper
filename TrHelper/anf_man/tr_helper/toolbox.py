import datetime
import requests
from collections import namedtuple
from io import BytesIO

from django.core.cache import cache

from bs4 import BeautifulSoup
from Levenshtein import distance, jaro_winkler
import PIL
from PIL import Image
import numpy as np

from .c.app_config import config_url
from .models import LANGUAGE_CHOICES, Article, ArticleCase

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
        NewArticle.compare_parse(self)

    def compare_parse(self):
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
    '''Check url and manage answer in order to url status'''

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

        return True

    def update(self):
        query = Article.objects.get(url=self.update_url)
        query.url = self.url
        query.title = self.title
        query.symbols_amount = self.symbols_amount
        query.save()

    def write_bd(self):
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
        if Manager.is_new(self):
            Manager.write_bd(self)
            return
        else:
            Manager.update(self)
            return


class FlowListener():
    '''Parse soup and in case of new url ask Manager class
    to check if it is new one'''

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

        try:
            num = urls.index(self.last)
            if num:
                url = urls[:num][-1]
                print(url)
                Manager(url=url).manage()
                with open(self.log, 'a') as log:
                    log.write(url+'\n')

        except ValueError:
            pass

# def create_user():
#     user = User.objects.create_user(username, email, password)
#     user.is_translator = True
#     user.save()
#
#     cloud_account = User.objects.create_user(username, passowrd)
#     cloud_account.save()
#     account = CloudAccount(user=user, account=cloud_account, folder_name='some_name')
#     account.save()

import os
import re
import errno
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

from tqdm import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




class PyMailCloudError(Exception):
    pass

    class AuthError(Exception):
        def __init__(self, message="Login or password is incorrect"):
            super(PyMailCloudError.AuthError, self).__init__(message)

    class NetworkError(Exception):
        def __init__(self, message="Connection failed"):
            super(PyMailCloudError.NetworkError, self).__init__(message)

    class NotFoundError(Exception):
        def __init__(self, message="File not found"):
            super(PyMailCloudError.NotFoundError, self).__init__(message)

    class PublicLinksExceededError(Exception):
        def __init__(self, message="Public links number exceeded"):
            super(PyMailCloudError.PublicLinksExceededError, self).__init__(message)

    class UnknownError(Exception):
        def __init__(self, message="WTF is going on?"):
            super(PyMailCloudError.UnknownError, self).__init__(message)

    class NotImplementedError(Exception):
        def __init__(self, message="The developer wants to sleep"):
            super(PyMailCloudError.NotImplementedError, self).__init__(message)
    class FileSizeError(Exception):
        def __init__(self, message="The file is bigger than 2 GB"):
            super(PyMailCloudError.FileSizeError, self).__init__(message)

__version__ =  "0.2"

class PyMailCloud:
    def __init__(self, login, password):

        self.user_agent = "PyMailCloud/({})".format(__version__) #should be changed
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        self.login = login
        self.password = password
        self.downloadSource = None
        self.uploadTarget = None
        self.__recreate_token()

    def __recreate_token(self):
        loginResponse = self.session.post("https://auth.mail.ru/cgi-bin/auth",
                                          data={
                                              "page": "http://cloud.mail.ru/",
                                              "Login": self.login,
                                              "Password": self.password
                                          },verify=False
                                          )
        # success?
        if loginResponse.status_code == requests.codes.ok and loginResponse.history:
            getTokenResponse = self.session.post("https://cloud.mail.ru/api/v2/tokens/csrf")
            if getTokenResponse.status_code is not 200:
                raise PyMailCloudError.UnknownError
            self.token = json.loads(getTokenResponse.content.decode("utf-8"))['body']['token']
            print('Login successful')
            self.__get_download_source()
        else:
            raise PyMailCloudError.NetworkError()


    def upload_callback(self, monitor, progress):
        progress.total = monitor.len
        progress.update(8192)
        pass

    def upload_files(self, file, file_name, folder_name):
        progress = tqdm(unit='B')
        progress.desc = file_name

        destination = '/' + folder_name + '/' + file_name
        # if os.path.getsize(file['filename']) > 1024 * 1024 * 1024 * 2:
        #     raise PyMailCloudError.FileSizeError
        monitor = MultipartEncoderMonitor.from_fields(
            fields={'file': ('filename', file, 'application/octet-stream')},
            callback=lambda monitor: self.upload_callback(monitor, progress))
        upload_response = self.session.post(self.uploadTarget, data=monitor,
                          headers={'Content-Type': monitor.content_type},verify=False)
        if upload_response.status_code is not 200:
            raise PyMailCloudError.NetworkError

        hash, filesize = upload_response.content.decode("utf-8").split(';')[0], upload_response.content.decode("utf-8").split(';')[1][:-2]
        response = self.session.post("https://cloud.mail.ru/api/v2/file/add",  # "http://httpbin.org/post",
                                     data={
                                         "token": self.token,
                                         "home": destination,
                                         "conflict": 'rename',
                                         "hash": hash,
                                         "size": filesize,
                                     })
        return json.dumps(response.json(), sort_keys=True, indent=3, ensure_ascii=False)
