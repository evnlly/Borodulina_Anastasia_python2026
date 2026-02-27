def plus_one(a):
    for i in range(len(a) - 1, -1, -1):
        if a[i] < 9:
            a[i] += 1
            return a
        a[i] = 0
        return [1] + [0] * len(a)


print(plus_one([4, 3, 2, 1]))
print(plus_one([8, 9, 9, 9]))