import openpyxl
import os, time

def get_tr_tabl(path):
    '''Open external table, populate the translation_table and
        diphthong_list  and return the variables.
        External table has two sheets: Singal and Diphthongs,
        each of them has two columns. They consist kurdish and
        relative russian sounds.
        Use openpyxl module.'''

    diphthong_list = []
    translation_table = {}

    wb = openpyxl.load_workbook(path)
    sheet_single = wb['Single']
    sheet_diphthongs =  wb['Diphthongs']
    for kurd, ru in tuple(sheet_single.rows):
        translation_table[kurd.value] = ru.value
    for kurd, ru in tuple(sheet_diphthongs.rows):
        diphthong_list.append(kurd.value)
        translation_table[kurd.value] = ru.value

    return diphthong_list, translation_table


class SingleTranslit():
    '''
        Implement logic of kurdish(kurmangi)-russian transliteration
        for singl word.
        Should be called as a function with word as argument.
        Return the translitirated word as a capitalized string.

        >> tr = Translit('Word')
        >> tr.translit()
        'Ворд'
    '''

    path = os.getcwd() + '/translit/logic/translit_rules.xlsx'
    time_m = os.path.getmtime(path)
    diphthong_list, tr_table = get_tr_tabl(path)

    def __init__(self, word):
        self.word = word

        ''' If time of last table modification is different -
            reload diphthong_list and translation_table.'''

        self.time = os.path.getmtime(SingleTranslit.path)
        print(SingleTranslit.time_m, self.time)
        if SingleTranslit.time_m != self.time:
            diphthong_list, tr_table = get_tr_tabl(SingleTranslit.path)
            time_m = self.time


    def break_word(self):
        '''
            Try to break word to peaces according exceptions
            to prepare word to transliteration.
            Return sounds_list.
        '''
        self.sounds_list = []
        for liter in self.word:
            try:
                #if pair liter+previouse is in translation_table -
                #we treat it as a diphthong and add together
                #to the list as one element
                pair = self.word[self.word.index(liter)-1] + liter
                SingleTranslit.tr_table[pair]

                self.sounds_list.pop()
                self.sounds_list.append(pair)
                #IndexError - if it is first liter
            except (IndexError, KeyError):
                self.sounds_list.append(liter)

        return self.sounds_list


    def translit(self):
        '''Extract apropriete russian sound from dictionary.
            Return the word as a capitalized string.'''

        SingleTranslit.break_word(self)

        self.rus = ''.join([
            SingleTranslit.tr_table[sound] if sound in SingleTranslit.tr_table \
            else sound for sound in self.sounds_list
            ])
        if self.rus[-1] == 'л':
            self.rus += 'ь'
        return self.rus



class RawTranslit():
    ''' res = RawTranslit(raw)
        raw
    '''

    def __init__(self, raw, user_dict=None):
        self.user_dict = user_dict
        self.info = ''
        self.split_list = [i for i in raw if not i.isalpha()]
        self.split_list = [i+' ' if i == ',' else i for i in self.split_list]
        self.raw = raw
        for sep in set(self.split_list):
            if sep:
                self.raw = self.raw.replace(sep, ' ')
        self.raw = self.raw.split()


    def in_dict(self, i):
        '''Check user_dict or make transliteration for single word,
            form info comment, if exist'''
        if self.user_dict:
            try:
                query = self.user_dict.objects.get(kurd=i)
                self.rus = query.ru
                info = query.info
                if info:
                    self.info += '{} (курд. {}) -- {}\n'.format(
                        self.rus,
                        i,
                        info
                        )

                return self.rus
            except self.user_dict.DoesNotExist:
                return False
        return False

    def __call__(self):
        self.res = []

        for i in self.raw:
            if RawTranslit.in_dict(self, i):
                self.res.append(self.rus)
            else:
                tr = SingleTranslit(i).translit()
                self.res.append(tr)

        sep_back = []
        print(self.split_list, self.res)
        for item, sep in zip(self.res[:-1], self.split_list):
            sep_back.append(item+sep)

        if self.res:
            sep_back.append(self.res[-1])
            res = ''.join(sep_back)
        else:
            res = ''.join(self.split_list)

        return res, self.info
