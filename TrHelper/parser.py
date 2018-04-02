from bs4 import BeautifulSoup
import requests
import string
import os
import sys
from abc import ABCMeta
from datetime import date

class LinkHandler(metaclass=ABCMeta):
    '''Abstract class for creation the handlers
    with particular behaviour
    to organize translators' work
    with different news' web-pages.'''

    handlers_dict = {}



    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(
                requests.get(self.url).text,
                'lxml'
                )


    def get_text(self):
        pass


    def form_path(name):
        '''Construct the path to store the parsed text in docx
        in directories inside cwd separetly for each day
        for Linux and Windows based system '''

        name = name

        slash_dict = dict(zip(('linux', 'win'), ('/', '\\')))

        if sys.platform.startswith('linux'):
            slash = slash_dict['linux']
        elif sys.platform.startswith('win'):
            slash = slash_dict['win']
        else:
            print(
                '''It looks like we will have trobles.
                We run only in Linux and Windows, but you have {}'''.format(
                sys.platform
                )
                )
        dirc = os.getcwd() + slash + date.today().strftime('%d.%m.%y')

        try:
            os.makedirs(
                dirc
                )
        except:
            pass



        path = r'{}{}{}{}'.format(dirc, slash, name, '.docx')

        print('\n\tIs storing in:\n\t\t{}\n\tFile name:\n\t\t{}'.format(
            dirc, name
            ))

        return path


    def write_docx(self):
        pass

    def count_simbols(self):
        pass

    def add_handler(web, handler_name):
        '''web - should be string,
           handler_name - should be class name
                          and subclass of LinkHandler class
        '''

        if issubclass(handler_name, LinkHandler):
            LinkHandler.handlers_dict[web] = handler_name
            return 'Handler is added'
        else:
            return 'Something goes wrong!'


class AnfLinkHandler(LinkHandler):
    '''Handler for ANFnews website'''

    def get_text(self):
        self.text = self.soup.find('article').get_text().splitlines()
        self.text = [line.strip('\t') for line in self.text if line]
        self.title = self.text[0]

        return self.text, self.title


    def write_docx(self):
        AnfLinkHandler.get_text(self)

        self.name = ''.join([
            self.title[i]
            for i in range(len(self.title))
            if self.title[i] not in string.punctuation
            ]).replace(' ', '_')

        self.path = LinkHandler.form_path(self.name)

        with open(self.path, 'w') as docx:
            for el in self.text:
                docx.write(el + '\n\n')
            docx.write(self.url)

        return print('\n\tWork is done!')


    def count_simbols(self):
        '''Count the number of symbols with spases
        from list of strings'''

        AnfLinkHandler.get_text(self)
        self.count = sum([len(line) for line in self.text])
        return self.count
