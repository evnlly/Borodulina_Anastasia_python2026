def two_sum(a, sum):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] + a[j] == sum:
                return [i, j]
    return 0


#отсортировано
def two_sum_faster(a, sum):
    left, right = 0, len(a) - 1
    while left < right:
        if sum > a[right] + a[left]:
            left += 1
        elif sum < a[right] + a[left]:
            right -= 1
        else:
            return [left, right]


print(two_sum_faster([2, 7, 11, 15], 9))
print(two_sum([4, 5, 9, 5], 10))
print(two_sum([-4, 3, 10, 0], -1))