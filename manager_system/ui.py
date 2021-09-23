"""
作者：zyy
日期：2021年08月02日
"""
from bll import *
from model import *


class StudentManagerView:
    '''
    学生信息系统视图
    '''

    def __init__(self):
        self.__manager = StudentManager()

    def __display_menu(self):
        """
        显示界面信息
        """
        print('1) 添加学生')
        print('2) 显示学生')
        print('3) 删除学生')
        print('4) 修改学生')
        print('5) 按照成绩升序显示学生信息')

    def __select_menu(self):
        """
        页面选择
        """
        choose = input('请选择：')
        if choose == '1':
            self.__input_student()
        elif choose == '2':
            self.__output_student()
        elif choose == '3':
            self.__del_student()
        elif choose == '4':
            self.__modify_student()
        elif choose == '5':
            self.sort_student_score()
        else:
            print('选择错误，重新选择！！！')

    def main(self):
        """
        界面视图入口
        """
        while True:
            self.__display_menu()
            self.__select_menu()

    def __input_error_manage(self, message):
        while True:
            try:
                number = float(input(message))
                return number
            except:
                print('输入信息格式不对，重新输入！！！！！！！')
        return info

    def __input_student(self):
        name = input('请输入姓名：')
        age = self.__input_error_manage('请输入年龄：')
        score = float(input('请输入成绩：'))
        stu = StudentModel(name, age, score)
        self.__manager.add_student(stu)

    def __output_student(self):
        for item in self.__manager.stu_list:
            print(item.id, item.name, item.age, item.score)

    def __del_student(self):
        id = int(input('请输入要删除学生的编号：'))
        if self.__manager.remove_student(id):
            print('删除成功')
        else:
            print('删除失败')

    def __modify_student(self):
        """
        修改信息
        """
        stu = StudentModel()
        stu.id = int(input('请输入要修改的学生编号：'))
        stu.name = input('请输入新的姓名：')
        stu.age = int(input('请输入新的年龄：'))
        stu.score = float(input('请输入新的成绩：'))
        if self.__manager.update_student(stu):
            print('修改成功')
        else:
            print('修改失败')

    def sort_student_score(self):
        # self.__manager.stu_list.sort(key=lambda student: student.score)
        newlist = sorted(self.__manager.stu_list, key=lambda student: student.score)
        for item in newlist:
            print(item.id, item.name, item.age, item.score)
