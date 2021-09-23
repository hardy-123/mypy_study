"""
作者：zyy
日期：2021年08月27日
"""
'''
    dict 服务端
        业务逻辑处理
        多进程 tcp 并发 process
'''
from socket import *
from multiprocessing import Process
import signal,sys
from mysql_db import Database
from time import sleep

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)
# 建立数据库对象
db = Database(host='47.98.173.117',
              port=3306,
              user='root',
              password='root',
              database='mydict',
              charset='utf8')

# 注册处理
def do_register(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    # 返回True表示注册成功，False 表示注册失败
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

# 登录处理
def do_login(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    # 返回True表示登录成功，False 表示登录失败
    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

# 查单词处理
def do_query(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]

    # 插入历史记录
    db.insert_hist(name,word)
    # 没找到返回None,找到返回单词解释
    mean = db.query(word)
    if not mean:
        c.send('没有找到该单词'.encode())
    else:
        msg = '%s : %s'%(word,mean)
        c.send(msg.encode())

# 查询历史记录
def do_hist(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    r = db.history(name)  # 数据库处理
    if not r:
        c.send(b'Fail')
        return
    c.send(b"OK")
    for i in r:
        # i -->是元组类型
        msg = "%s %-16s %s"%i  # %-16s  表示左对齐占16个字节
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b"##")  # 发送结束标志

# 接收客户端请求，分配处理
def request(c):
    cur = db.create_cursor()  # 每个子进程单独生成游标
    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            sys.exit()  # 对应的子进程退出
        elif data[0] =='R':
            do_register(c,data)
        elif data[0] == 'L':
            do_login(c,data)
        elif data[0] == 'Q':
            do_query(c,data)
        elif data[0] == 'H':
            do_hist(c,data)


# 搭建网络，固定的框架
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)  # 把僵尸进程丢给操作系统处理

    # 循环等待客户端连接
    print('listen the port 8888...')
    while True:
        try:
            c, addr = s.accept()
            print('connect from', addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('服务端退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程处理客户端事务
        p = Process(target=request, args=(c,))
        p.daemon = True  # 父进程结束则所有服务终止
        p.start()


if __name__ == '__main__':
    main()