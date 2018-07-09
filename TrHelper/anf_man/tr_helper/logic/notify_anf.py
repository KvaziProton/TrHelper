import requests
from bs4 import BeautifulSoup
import notify2
from handlers import handler as p
import os


class ANFNotify():
    '''Create a notification about new articles in ANFnews
    website. Has dependency from module "handler" (count number
    of symbols and parse the title)'''

    def __init__(self, url=''):
        self.url = 'https://anfenglish.com/latest-news'


    def get_info(self):
        '''Try to parse the page with all articles and get info
        about last one, return the title and the link'''

        try:
            self.soup = BeautifulSoup(
                requests.get(self.url).text,
                'lxml'
                )

        except OSError:
            self.message = '''
There is no Internet connection, monitoring is stoped!

Check Internet connection and
try again later.
            '''
            self.ICON_PATH = os.getcwd() + '/static/siren.png'
            self.notify_title = 'Connection was lost!'

        except IndexError:
            self.message = '''
Fucking capcha again!!!
            '''
            self.ICON_PATH = os.getcwd() + '/static/siren.png'
            self.notify_title = 'Are you robot??!'

        else:
            self.blocks = self.soup.find_all('tr')[1]

            self.link = self.blocks.find('a').get('href')
            self.time = self.blocks.find('td').get_text()
            parser = p.AnfLinkHandler(self.link)
            *first, self.title = parser.get_text()
            self.count = parser.count_simbols()

            self.message = '{}\n\n{}\n\n{} symbols'.format(
                self.time, self.title, self.count
                )
            self.ICON_PATH = os.getcwd() + '/static/alarm.png'
            self.notify_title = "New ANF article!"

            return self.title, self.link, self.count
