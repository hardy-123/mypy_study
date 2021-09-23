"""
作者：zyy
日期：2021年08月02日
"""


class StudentManager:
    """
    行为方法
    """
    # 类变量，初始编号
    __init_id = 1000

    def __init__(self):
        self.__stu_list = []

    @property
    def stu_list(self):
        return self.__stu_list

    def add_student(self, stu_info):
        """
            添加一个新学生
        :param stu_info: 没有编号的学生信息
        """
        stu_info.id = self.__generate_id()
        self.stu_list.append(stu_info)

    def __generate_id(self):
        """
        生成编号
        """
        StudentManager.__init_id += 1
        return StudentManager.__init_id

    def remove_student(self, id):
        """
        根据编号删除学生
        :param id: 学生编号
        :return:
        """
        for stu in self.__stu_list:
            if stu.id == id:
                self.__stu_list.remove(stu)
                return True  # 表示移除成功
        return False  # 表示移除失败

    def update_student(self, stu_info):
        """
        修改学生信息
        :param stu_info: 学生列表
        :return:
        """
        for stu in self.__stu_list:
            if stu.id == stu_info.id:
                stu.score = stu_info.score
                stu.name = stu_info.name
                stu.age = stu_info.age
                return True  # 表示修改成功
        return False  # 表示修改失败