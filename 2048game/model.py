"""
作者：zyy
日期：2021年08月07日
"""
"""
    数据模块
"""
class DirectionModel:
    """
        方向数据模型
        枚举  常量-->（命名全部大写）
    """
    # 给数配一个字，在整数基础上，添加一个人容易识别的'标签'
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Location:
    """
        位置
    """
    def __init__(self,r,c):
        self.c_index = c
        self.r_index = r
