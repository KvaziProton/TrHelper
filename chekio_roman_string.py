def reverse_roman(rs):
    num = ('I', 'V', 'X', 'L', 'C', 'D', 'M')
    val = (1, 5, 10, 50, 100, 500, 1000)
    table = dict(zip(num, val))
    rs = list(table[i] for i in rs)
    res = 0
    while rs:
        if len(rs) == 1 or rs[0] >= rs[1]:
            res += rs[0]
            rs.remove(rs[0])
        else:
            res += rs[1] - rs[0]
            rs = rs[2:]
    return res



print(reverse_roman('MMMDCCCLXXXVIII'))

'''


def reverse_roman(n):

    result = 0

    for roman, arabic in zip('CM   CD   XC  XL  IX IV M     D    C    L   X   V  I'.split(),

                             (900, 400, 90, 40, 9, 4, 1000, 500, 100, 50, 10, 5, 1)):

        result += n.count(roman)*arabic

        n = n.replace(roman, '')

    return result

'''
