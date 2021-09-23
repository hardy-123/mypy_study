"""
作者：zyy
日期：2021年08月27日
"""
import sys

'''
    dict 客户端
    根据用户输入，发送请求，得到结果
    结构： 一级界面  --> 注册  登录   退出
          二级界面  --> 查单词  历史记录  注销
'''
import os
from socket import *
from getpass import getpass  # 运行使用终端

# 服务器地址
ADDR = ('127.0.0.1',8000)  # 地址
s = socket()  # 默认是tcp套接字
s.connect(ADDR)  # 连接

# 查单词
def do_query(name):
    while True:
        word = input("输入单词：")
        if word == "##":  # 接收单词查询
            break
        msg = "Q %s %s"%(name,word)
        s.send(msg.encode())  # 发送请求
        # 得到查询结果
        data = s.recv(2048).decode()
        print(data)

# 查询历史记录
def do_hist(name):
    msg = "H " + name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print('您还没有历史记录')

# 二级界面
def login(name):
    while True:
        # os.system('clear')
        print("""
        ==============Query=============
        *                              *
        * 1.查单词  2.历史记录  3.注销 *
        *                              *
        ================================
        """)
        cmd = input('输入选项：')
        if cmd == '1':
            do_query(name)
        elif cmd =='2':
            do_hist(name)
        elif cmd =='3':
            return
        else:
            print('请输入正确选项')

# 注册
def do_register():
    while True:
        name = input('User:')
        passwd = getpass('Passwd:')
        passwd1 = getpass('Passwd Again:')
        if passwd != passwd1:
            print('两次密码不一致！')
            continue
        if ' ' in name or ' ' in passwd:
            print('用户名密码不能有空格')
            continue
        msg = "R %s %s"%(name,passwd)
        s.send(msg.encode())  # 发送给服务器
        data = s.recv(128).decode()  # 接收结果
        if data == 'OK':
            print('注册成功')
            login(name)
        else:
            print('注册失败')
        return

#登录
def do_login():
    name = input('User:')
    passwd = getpass('Passwd:')
    msg = "L %s %s"%(name,passwd)
    s.send(msg.encode())  # 发送请求
    data = s.recv(128).decode()  # 得到回复
    if data == 'OK':
        print('登录成功')
        login(name)
    else:
        print('登录失败')

# 搭建客户端网络
def main():
    while True:
        # os.system('clear')
        print("""
        ============Welcome=============
        *                              *
        *   1.注册   2.登录   3.退出   *
        *                              *
        ================================
        """)
        cmd = input('输入选项：')
        if cmd == '1':
            do_register()
        elif cmd =='2':
            do_login()
        elif cmd =='3':
            s.send(b'E')
            sys.exit("谢谢使用！")
        else:
            print('请输入正确选项')


if __name__ == '__main__':
    main()

