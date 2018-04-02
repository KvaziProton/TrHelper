def mygcd(x, y):
    if x > y:
        lst = []
        ost = 1
        while ost != 0:
            part = x // y
            ost = x % y
            y
            lst.append(part)
            print(lst)
        else:
            x, y = y, x

print(mygcd(69025142, 10927782))
