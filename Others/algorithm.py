# 算法algorithm
# 汉诺塔
def hanoi(n, x, y, z):
    if n == 1:
        print(x, '-->', z)
    else:
        hanoi(n - 1, x, z, y)
        hanoi(1, x, y, z)
        hanoi(n - 1, y, x, z)


n = int(input('请输入汉诺塔的层数：'))
hanoi(n, 'x', 'y', 'z')


# 杨辉公式
def triangles(n):
    lst = [1]
    for j in range(n):
        print(lst)
        lst.append(0)
        lst = [lst[i - 1] + lst[i] for i in range(len(lst))]


triangles(3)
