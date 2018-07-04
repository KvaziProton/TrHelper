import openpyxl
import os, time

def is_integral(name):
    '''
        Return true or false
    '''

    name = name[0].lower() + name[1:]

    return not name.islower()


def integral_term(translit_term_class):
    def wrapper(term, user_dict=None):
        sep_back = []
        if is_integral(term):
            split_list = [i for i in term if not i.isalpha()]
            split_list = [i+' ' if i == ',' else i for i in split_list ]
            for sep in set(split_list):
                if sep != ' ':
                    term = term.replace(sep, ' ')
            pr_list = term.split()
            case_list = [item.islower() for item in pr_list]
            tr = translit_term_class
            tr.dict = user_dict
            res_list = [tr(item.lower()) for item in pr_list ]


            case_back = [item if case else item.capitalize() for item, case in zip(res_list, case_list)]
            for item, sep in zip(case_back[:-1], split_list):
                sep_back.append(item+sep)
            sep_back.append(case_back[-1])
            res = ''.join(sep_back)

            return res

        tr = translit_term_class(term)
        tr.user_dict = user_dict
        res = tr()
        print(res)
        return res.capitalize() #, info
    return wrapper


def get_tr_tabl(path):
    '''
        Open external table, populate the translation_table and
        diphthong_list  and return the variables.
        External table has two sheets: Singal and Diphthongs,
        each of them has two columns. They consist kurdish and
        relative russian sounds.
        Use openpyxl module.
    '''

    diphthong_list = []
    translation_table = {}

    wb = openpyxl.load_workbook(path)
    sheet_single = wb['Single']
    sheet_diphthongs =  wb['Diphthongs']
    for kurd, ru in tuple(sheet_single.rows):
        translation_table[kurd.value.lower()] = ru.value.lower()
    for kurd, ru in tuple(sheet_diphthongs.rows):
        diphthong_list.append(kurd.value)
        translation_table[kurd.value] = ru.value

    return diphthong_list, translation_table

# @integral_term
class Translit():
    '''
        Implement logic of kurdish(kurmangi)-russian transliteration
        for singl word.
        Should be called as a function with word as argument.
        Return the translitirated word as a capitalized string.

        >> tr = Translit()
        >> tr()
        'Ворд', []
    '''
    def __init__(self, term, user_dict = None):
        self.word = term
        self.user_dict = user_dict
    path = os.getcwd() + '/translit/logic/translit_rules.xlsx'
    time_m = os.path.getmtime(path)
    diphthong_list, translation_table = get_tr_tabl(path)

    # def __tab_check(self):
    #     '''
    #         If time of last table modification is different -
    #         reload diphthong_list and translation_table
    #
    #     '''
    #
    #     self.time = os.path.getmtime(Translit.path)
    #     if Translit.time_m != self.time:
    #         diphthong_list, translation_table = get_tr_tabl(Translit.path)
    #         time_m = self.time



    def dict_check(self):
        '''
            Check user_dict or make transliteration for single word,elem
            form info commect, if exist
        '''
        if self.user_dict:
            try:
                query = self.user_dict.objects.get(kurd=self.word)
                self.rus = query.ru
                info = query.info
                if info:
                    self.info = ('{} (курд. {})\n'.format(self.rus, self.word))

                return self.rus
            except self.user_dict.DoesNotExist:
                return False
        return False


    def __break_word(self):
        '''
            Try to break word to peaces according exceptions
            to prepare word to transliteration.
            Return sounds_list.
        '''

        for liter in self.word:
            try:
                #if pair liter+previouse is in translation_table -
                #we treat it as a diphthong and add together
                #to the list as one element
                pair = self.word[self.word.index(liter)-1] + liter
                Translit.translation_table[pair]

                self.sounds_list.pop()
                self.sounds_list.append(pair)
                #IndexError - if it is first liter
            except (IndexError, KeyError):
                self.sounds_list.append(liter)

        return self.sounds_list


    def __translit(self):
        '''
            Extract apropriete russian sound from dictionary.
            Return the word as a capitalized string.
        '''

        self.rus = ''.join([
            Translit.translation_table[sound] if sound in Translit.translation_table else sound for sound in self.sounds_list
            ])
        # if self.rus[-1] == 'л':
        #     self.rus += 'ь'
        return self.rus


    def __call__(self):
        '''
            Prepare word to transliteration (change case to low).
            Make up the order of calling methods.
        '''
        # Translit.__tab_check(self)
        self.info = None

        self.sounds_list = []


        if not Translit.dict_check(self):
            Translit.__break_word(self)
            Translit.__translit(self)

        return self.rus
