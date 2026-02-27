def brackets(s):
    a = []
    for _ in s:
        if _ == '(':
            a.append('(')
        elif _ == ')':
            if len(a) == 0:
                return False
            else:
                a.pop()
    return len(a) == 0


print(brackets('()'))