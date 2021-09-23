"""
作者：zyy
日期：2021年08月29日
"""
'''
    webframe  模拟后端应用工作流程
        
        从httpserver接收具体请求
        根据请求进行逻辑处理和数据处理
        将需要的数据反馈给httpserver
'''
import json
from socket import *
from settings import *
from select import select
from urls import *

# 应用类，处理某一方面的请求
class Application:
    def __init__(self):
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        self.sockfd.bind((frame_ip,frame_port))

    # 启动服务
    def start(self):
        self.sockfd.listen(5)
        print('Start app listen %s'%frame_port)
        self.rlist.append(self.sockfd)
        # select 监控请求
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sockfd:
                    connfd,addr = r.accept()
                    self.rlist.append(connfd)
                else:
                    self.handle(r)
                    self.rlist.remove(r)

        # while True:
        #     c, addr = self.sockfd.accept()
        #     data = c.recv(1024).decode()
        #     print(json.loads(data))
        #     d = {'status': '200', 'data': 'xxxxxxx'}
        #     c.send(json.dumps(d).encode())

    # 处理具体的httpserver请求
    def handle(self,connfd):
        request = connfd.recv(1024).decode()
        request = json.loads(request)
        # request => {'method': 'GET', 'info': '/xx'}
        if request['method'] == 'GET':
            if request['info'] == '/' or request['info'][-5:] == '.html':
                response = self.get_html(request['info'])
            else:
                response = self.get_data(request['info'])
        elif request['method'] == 'POST':
            pass
        # 将数据发送给httpserver
        # response=>{'status': '200', 'data': 'xxxxxxx'}
        # print(response)
        response = json.dumps(response)
        connfd.send(response.encode())
        connfd.close()

    # 获取网页
    def get_html(self,info):
        if info == '/':
            filename = DIR + '/index.html'
        else:
            filename = DIR + info
        # print(filename)
        try:
            f = open(filename, 'rb')
        except Exception:
            response = '<h1>Sorry.....no found filename</h1>'
        else:
            response = f.read().decode()
        finally:
            # 返回对应的数据格式
            return {'status': '200', 'data': response}

    # 返回其他内容
    def get_data(self,info):
        for url,func in urls:
            if url == info:
                return {'status': '200', 'data': func()}
        return {'status': '404', 'data': '<h1>Sorry...I can not do it</h1>'}


app = Application()
app.start()





