print(int(input())//10)

print(input()[-2])

a, b, c = input()
print(int(a) + int(b) + int(c)))

print('A'*100)

h, m = divmod(int(input()), 60)
if h > 23:
    h //= 24
    h -= 1
print('{} {}'.format(h, m))

num = int(input())
data = (
 r'   _~_    ',
 r'  (o o)   ',
 r' /  V  \  ',
 r'/(  _  )\ ',
 r'  ^^ ^^   '
 )
 for line in data:
     print(line*num, sep=' ')

rub = int(input())
kop = int(input())
n = int(input())
kop += rub*100
rub, kop = divmod((kop*n), 100)
print('{} {}'.format(rub, kop))

num = int(input())
print(
    '''
    The next number for the number {num} is {next}.\t
    The previous number for the number {num} is {prev}.
    '''
    .format(num=num, next=num - 1, prev=num + 1)
    )

v = int(input())
t = int(input())
trac = (v * t) % 109
print(trac) if v > 0 else print(109 - trac)

a = input()
print(1) if a == '0' or a[:2] == a[2:][::-1] else print(2)
