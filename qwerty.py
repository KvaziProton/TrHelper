
def change_kb(raw):
    eng = list("qwertyuiop[]asdfghjkl;'\zxcvbnm,./"+
               'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?')
    ru = list("йцукенгшщзхъфывапролджэ\ячсмитьбю."
            +'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,')
    return ''.join(dict(zip(eng, ru))[x] for x in raw)
