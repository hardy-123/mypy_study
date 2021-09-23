"""
作者：zyy
日期：2021年08月18日
"""
from socket import *
import os,sys

ADDR = ('127.0.0.1',8888)

# 发送消息
def send_msg(s,name):
    while True:
        try:
            text = input('发言：')
        except KeyboardInterrupt:
            text = 'quit'
        if text.strip() == 'quit':
            msg = "Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit('退出聊天室')
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),ADDR)

# 接收消息
def recv_msg(s):
    while True:
        try:
            data,addr = s.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode() + '\n发言：',end='')

def main():
    s = socket(AF_INET,SOCK_DGRAM)
    # 进入聊天室
    while True:
        name = input('请输入姓名：')
        msg = 'L ' + name
        s.sendto(msg.encode(),ADDR)
        # 接收反馈
        data,addr = s.recvfrom(128)
        if data.decode() == 'OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())

    # 已经进入聊天室了
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s,name)  # 子进程负责发送消息
    else:
        recv_msg(s)  # 父进程负责消息接收


main()