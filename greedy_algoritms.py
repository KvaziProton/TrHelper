# n = int(input())
# sec_list = [[int(x) for x in input().split()] for i in range(n)]
#
#
# def cover_sector_by_points(sec_list):
#     sec_list = sorted(sec_list, key = lambda x: x[1])
#     points = [sec_list[0][1],]
#     for coord in sec_list[1:]:
#         if points[-1] not in range(coord[0],coord[1]+1):
#             points.append(coord[1])
#     a = len(points)
#     res = [str(x) for x in points]
#     b = ' '.join(res)
#
#     return a, b
#
# a, b = cover_sector_by_points(sec_list)
#
# print('{}\n{}'.format(a, b))
#
#
# n, w = int(input().split())
# sub_list = [[int(a) for a in input().split()] for i in range(n)]
# res = [a/b for a, b in sub_list]
#
# res = reversed(sorted(res))

#
# n, w = map(int, input().split())
# d = {}
# for i in range(n):
#     c, v = map(int, input().split())
#     d[c/v] = v
#
# lst = sorted(list(d.keys()), reverse=True)
# count = 0
# for x in range(n):
#     i = lst[x]
#     v = d[i]
#     w -= v
#     count += i*v
#     if w == 0:
#         break
#     elif w < 0:
#         count += i*w
#         break
#
#
# print('{:.3f}'.format(count))
#
#
#
#
# n = int(input())
# lst = []
# i = 0
# while n > 0:
#     i += 1
#     n -= i
#     lst.append(i)
# if n < 0:
#     lst.pop()
#     lst[-1] += i + n
#
# print(len(lst))
# print(*lst)

raw = input()
freq_list = sorted([(raw.count(i), i) for i in set(raw)], reverse=True)
count = 0
code_dict = {}
l = len(freq_list)
if l == 1:
    code_dict[freq_list[0][1]] = '0'
else:
    f = freq_list[:-1]
    for freq, val in f:
        code_dict[val] = '1' * count + '0'
        count += 1
        f = sorted(f, reverse=True)
    code_dict[freq_list[-1][1]] = '1' * (l-1)

res = ''.join([code_dict[i] for i in raw])

print(l, len(res))
for key in sorted(code_dict.keys()):
    print('{}: {}'.format(key, code_dict[key]))
print(res)
