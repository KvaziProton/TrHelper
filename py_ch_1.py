# py-challenge first level

# import string
#
# raw = '''g fmnc wms bgblr rpylqjyrc gr zw fylb.
# rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb
# gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm
# jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb.
# lmu ynnjw ml rfc spj.'''
#
#
# # First attempt
# alf = string.ascii_lowercase + "ab"
# res = []
# for a in raw:
#     if a in alf:
#         res.append(alf[alf.index(a)+2])
#     else:
#         res.append(a)
# print(''.join(res))
#
# # List comprehention improvment
# alf = string.ascii_lowercase + "ab"
# lst = [alf[alf.index(a)+2] for a in raw if a in alf]
# print(lst)
#
#DIY translation
frm = string.ascii_lowercase + ",. '()"
t = string.ascii_lowercase[2:] + 'ab' + ",. '()"
''.join([dict(zip(frm, t))[x] for x in raw])

#Biuld-in translation
table = str.maketrans(string.ascii_lowercase, (string.ascii_lowercase[2:] + 'ab'))
print(raw.translate(table))
