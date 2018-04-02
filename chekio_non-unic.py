def chekio(ls):
    for i in ls[:]:
        if ls.count(i) < 2:
            ls.remove(i)        
    return ls

print(chekio([1, 2, 3, 4, 5]))
