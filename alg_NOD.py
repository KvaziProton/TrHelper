def nod(x, y):
    if x < y: x, y = y, x
    ost = x % y
    if ost == 0:
        return y
    else:
        nod(y, ost)

print(nod(69025142, 10927782))
