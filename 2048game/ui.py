"""
作者：zyy
日期：2021年08月07日
"""
'''
    2048 控制台界面
'''
import os  # 导入os模块
from bll import GameCoreController
from model import DirectionModel


class GameConsoleView:
    def __init__(self):
        self.__controller = GameCoreController()

    def main(self):
        self.__start()
        self.__update()

    def __start(self):
        # 产生两个数字
        self.__controller.get_new_number()
        self.__controller.get_new_number()
        # 绘制界面
        self.__draw_map()

        pass

    def __draw_map(self):
        # 绘制界面
        os.system('cls')  # 执行cls命令清空Python控制台
        for line in self.__controller.map:
            for item in line:
                print(item, end=" ")
            print()

    def __update(self):
        # 循环
        while True:
            # i = os.system('cls')  # 执行cls命令清空Python控制台
            # 判断玩家的输入  -->移动地图
            self.__move_move_for_input()
            # 产生新数字
            self.__controller.get_new_number()
            # 绘制界面
            self.__draw_map()
            # 游戏结束判断  -->提示
            if self.__controller.is_game_over():
                print('游戏结束')
                break



    def __move_move_for_input(self):
        while True:
            dir = input("请输入方向(wasd):")
            dict_dir = {
                "w":DirectionModel.UP,
                "a":DirectionModel.LEFT,
                "s":DirectionModel.DOWN,
                "d":DirectionModel.RIGHT
            }
            if dir in dict_dir:
                self.__controller.move(dict_dir[dir])
                break
            else:
                print('输入错误，重新输入！')


if __name__ == "__main__":
    view = GameConsoleView()
    view.main()
