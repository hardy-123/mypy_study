"""
作者：zyy
日期：2021年07月22日
"""
from typing import List, Any

'''
    2048 核心算法
'''
list_merge = [8, 8, 8, 8]

# 1.零元素移至末尾
#   [2,0,2,0] --> [2,2,0,0]
#   [2,0,0,2] --> [2,2,0,0]
#   [2,4,0,2] --> [2,4,2,0]

'''
# def zero_to_end(lists):
#     list1 = [0, 0, 0, 0]
#     # 从后往前，不是0就加入新列表，之后截取返回给列表
#     for i in lists[::-1]:
#         if i != 0:
#             list1.insert(0, i)
#     lists = list1[0:4]
#     return lists
# list_merge = zero_to_end(list_merge)
# print(list_merge)
'''


def zero_to_end():
    # 从前向后，如果发现零元素，删除并追加
    for i in range(-1, -len(list_merge) - 1, -1):
        if list_merge[i] == 0:
            del list_merge[i]
            list_merge.append(0)


# zero_to_end()
# print(list_merge)


# 2.零元素移至末尾
#   [2,0,2,0] --> [4,0,0,0]
#   [2,2,2,2] --> [4,4,0,0]
#   [2,2,0,2] --> [4,2,0,0]
def merge():
    """
    合并
    :return:
    """
    # 先将中间的零元素移到末尾
    # 再合并相邻相同元素
    zero_to_end()
    # print(list_merge)
    for i in range(len(list_merge) - 1):
        if list_merge[i] == list_merge[i + 1]:
            # 将后一个累加到前一个上
            list_merge[i] += list_merge[i + 1]
            del list_merge[i + 1]
            list_merge.append(0)


# merge()
# print(list_merge)

# 3.地图向左移动，把元素都给list_merge
map = [
    [2, 0, 0, 2],
    [0, 4, 2, 2],
    [2, 4, 0, 4],
    [2, 2, 4, 0],
]


def move_left():
    """
        向左移动
    :return:
    """
    # 思想：将二维列表中每行（从左到右）交给merge函数进行操作
    global list_merge
    for line in map:
        list_merge = line
        merge()


# move_left()
# print(map)


def move_right():
    """
        向右移动
    :return:
    """
    # 思想：将二维列表中每行（从右到左）交给merge函数进行操作
    global list_merge
    for line in map:
        # 从右向左取出数据 形成 新列表
        list_merge = line[::-1]  # line 产生新列表了，没给list_merge原来map的地址
        merge()
        line[::-1] = list_merge  # 还回给map


# move_right()
# print(map)

# 4.向上移动 向下移动
# 利用方阵转置函数
def zz():  # 转置,连转两次会回到原来（4*4方阵）
    map2 = []
    for i in range(4):  # 原矩阵的列
        map1 = []
        for j in range(4):  # 原矩阵的行
            a = map[j][i]
            map1.append(a)
        map2.append(map1)
    map[:] = map2

"""
def zz(sqr_matrix):
    for c in range(1, len(sqr_matrix)):
        for r in range(c, len(sqr_matrix)):
            sqr_matrix[r][c - 1], sqr_matrix[c - 1][r] = sqr_matrix[c - 1][r], sqr_matrix[r][c - 1]
"""

# print(map)
# zz()
# print(map)
# zz()
# print(map)


# 向上移动
def move_up():
    zz()
    move_left()
    zz()


# print(map)
# move_up()
# print(map)

# 向下移动
def move_down():
    zz()
    move_right()
    zz()


print(map)
move_down()
print(map)
