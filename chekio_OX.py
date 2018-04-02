def checkio(gr):
    col = [''.join(gr[i][y] for i in range(3)) for y in range(3)]
    d1 = [''.join([gr[i][i] for i in range(3)])]
    d2 = [''.join([gr[abs(i+1)][i] for i in range(-1, -4, -1)])]

    for el in col + d1 + d2 + gr:
        if el == el[0]*3 and el[0] != '.':
            return el[0]
    return 'D'




gr = [
    "OO.",
    "XOX",
    "XOX"]

print(checkio(gr))
