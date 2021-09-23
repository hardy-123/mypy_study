"""
作者：zyy
日期：2021年08月07日
"""
import random

from model import DirectionModel
from model import Location

'''
    游戏逻辑控制器
    负责处理 2048 核心算法
'''


class GameCoreController:
    def __init__(self):
        self.__list_merge = None
        self.__list_empty_location = []
        self.__map = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

    @property
    def map(self):
        return self.__map

    # @map.setter
    # def map(self,value):
    #     self.__map = value

    # 1.零元素移至末尾
    def __zero_to_end(self):
        # 从前向后，如果发现零元素，删除并追加
        for i in range(-1, -len(self.__list_merge) - 1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)
    
    # 2.零元素移至末尾
    def __merge(self):
        """
        合并
        """
        # 先将中间的零元素移到末尾
        # 再合并相邻相同元素
        self.__zero_to_end()
        # print(self.list_merge)
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                # 将后一个累加到前一个上
                self.__list_merge[i] += self.__list_merge[i + 1]
                del self.__list_merge[i + 1]
                self.__list_merge.append(0)
    
    def __move_left(self):
        """
            向左移动
        :return:
        """
        # 思想：将二维列表中每行（从左到右）交给merge函数进行操作
        for line in self.__map:
            self.__list_merge = line
            self.__merge()

    def __move_right(self):
        """
            向右移动
        :return:
        """
        # 思想：将二维列表中每行（从右到左）交给merge函数进行操作
        for line in self.__map:
            # 从右向左取出数据 形成 新列表
            self.__list_merge = line[::-1]  # line 产生新列表了，没给self.list_merge原来self.map的地址
            self.__merge()
            line[::-1] = self.__list_merge  # 还回给self.map

    def __matrix__transpose(self):
        for c in range(1,len(self.__map)):
            for r in range(c,len(self.__map)):
                self.__map[r][c-1],self.__map[c-1][r] = self.__map[c-1][r],self.__map[r][c-1]

    def __move_up(self):
        self.__matrix__transpose()
        self.__move_left()
        self.__matrix__transpose()
    
    def __move_down(self):
        self.__matrix__transpose()
        self.__move_right()
        self.__matrix__transpose()

    def move(self,dir):
        """
            移动
        :param dir: 方向，DirectionModel 类型
        """
        if dir == DirectionModel.UP:
            self.__move_up()
        elif dir == DirectionModel.DOWN:
            self.__move_down()
        elif dir == DirectionModel.LEFT:
            self.__move_left()
        elif dir == DirectionModel.RIGHT:
            self.__move_right()

    def get_new_number(self):
        """
            产生新数字
        """
        # 找到所有空白位置的索引
        self.__get_empty_location()
        # 选一个随机的空白位置
        if len(self.__list_empty_location)==0:
            return
        loc = random.choice(self.__list_empty_location)
        re = 4 if random.randint(1,10)==1 else 2
        self.__map[loc.r_index][loc.c_index] = re
        # 空位置已经生成元素，所有记录空位值的列表要把该位置移除
        self.__list_empty_location.remove(loc)

    def __get_empty_location(self):
        """
            统计空的位置
        """
        # 先清空列表再进行统计空位置
        self.__list_empty_location.clear()
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])):
                if self.__map[r][c] == 0:
                    self.__list_empty_location.append(Location(r,c))

    def is_game_over(self):
        """
            游戏是否结束
        :return: False 表示没有结束
        """
        # 是否有空位置
        if len(self.__list_empty_location)>0:
            return False
        # 判断横向竖向有没有相同元素
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])-1):
                if self.__map[r][c] == self.__map[r][c+1] or self.__map[c][r] == self.__map[c+1][r]:
                    return False
        return True


# 测试代码
if __name__ == "__main__":
    controller = GameCoreController()
    # controller.move(DirectionModel.UP)
    print(controller.map)
    controller.get_new_number()
    print(controller.is_game_over())
    # print(controller.map)
