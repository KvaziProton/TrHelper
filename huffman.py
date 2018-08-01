class Node():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def walk(self, code, acc):
        self.left.walk(code, acc+'0')
        self.right.walk(code, acc+'1')

class Leaf():
    def __init__(self, val):
        self.val = val

    def walk(self, code, acc):
        code[self.val] = acc or '0'


raw = input()
freq_list = []
for i in set(raw):
    freq_list.append((raw.count(i), len(freq_list), Leaf(i)))
freq_list = sorted(freq_list, key=lambda tup:tup[:-1], reverse=True)
l = len(freq_list)
huf_dict = {}
count = 0
while len(freq_list) > 1:
    freq1, _c1, left = freq_list.pop()
    freq2, _c2, right = freq_list.pop()
    new_freq = freq1 + freq2

    node = Node(left=left, right=right)
    freq_list.append((new_freq, count, node))
    count += 1
    freq_list = sorted(freq_list, key=lambda tup:tup[:-1], reverse=True)


[(_f, _c, root)] = freq_list
root.walk(huf_dict, '')

res = ''.join([huf_dict[i] for i in raw])

print(l, len(res))
for key in sorted(huf_dict.keys()):
    print('{}: {}'.format(key, huf_dict[key]))
print(res)
