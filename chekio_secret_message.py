# def und(text):
#     return ''.join(x for x in text if x.isupper())
#
# print(und('How are you? Eh, ok. Low or Lower? Ohhh'))

def count_words(text, words):
    return sum(x in text.lower() for x in words)

print(count_words('How aresjfhdskfhskd you?', ["how","are","you","hello"]))
