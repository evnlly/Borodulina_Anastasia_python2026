text = input()
dct = {}
for _ in text:
    if _ in dct:
        dct[_] += 1
    else:
        dct[_] = 1
print(dct)