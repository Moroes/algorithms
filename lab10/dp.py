from random import randint
import sys


def DP(s, a):
    dp = [1] + [0] * s

    for i in a:
        for j in range(s, -1, -1):
            if j - i >= 0 and dp[j - i] == 1:
                dp[j] = 1

    # print(dp) # Вывод получившихся заполняемостей рюкзака в виде [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0] s = 14
    i = s
    while dp[i] == 0:
        i -= 1
    # print(i) # Вывод максимальной вместительности рюкзака

    # восстановление ответа
    dp = [1] + [0] * s

    prev = [-1] * (s + 1)
    for i in a:
        for j in range(s, -1, -1):
            if j - i >= 0 and dp[j - i] == 1:
                dp[j] = 1
                prev[j] = i

    # print(dp) # [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
    # print(prev) # [-1, -1, -1, 3, -1, 5, -1, 7, 5, -1, 10, -1, 7, 10, -1]
    i = s
    while dp[i] == 0:
        i -= 1
    # print(i) # Вывод максимальной вместительности рюкзака

    mxsum = i
    ans = []
    while mxsum > 0:
        ans.append(prev[mxsum])
        mxsum -= prev[mxsum]
        
    # print(ans) # Вывод камней в куче
    return ans

for i in range(5):
    n = randint(1, 7)
    a = []
    for j in range(n):
        a.append(randint(1, 10))
    print(f"Общая куча = {a}")
    s = sum(a)
    print(f"Сумма общей кучи = {s}")
    ans = DP(round(s/2), a)
    for i in ans:
        if i in a:
            a.remove(i)
    print(f"Первая куча = {ans}")
    print(f"Вторая куча = {a}")
    print("Разница двух куч = ", abs(sum(a) - sum(ans)))
    print()

for i in ans:
    if i in a:
        a.remove(i)

