"""
作者：zyy
日期：2021年08月29日
"""
import json

'''
    httpserver 部分的主程序：
        获取http请求
        解析http请求
        将请求发送给webframe
        从webframe接收反馈数据
        将数据组织为response格式发送给客户端
'''
from socket import *
import sys
from threading import Thread
from config import *
import re,json

# 服务器地址
ADDR = (HOST,PORT)

# 和 webframe 通信从函数
def connect_frame(env):
    s =socket()
    try:
        s.connect((frame_ip,frame_port))
    except Exception as e:
        print(e)
        return
    # 将字典转换为json
    data = json.dumps(env)
    # 将解析后的请求发送给webframe
    s.send(data.encode())
    # 接收来自webframe数据
    data = s.recv(4096*100).decode()
    return json.loads(data)

# 将httpserver基本功能封装为类
class HTTPServer:
    def __init__(self):
        self.address = ADDR
        self.create_socket()  # 和浏览器交互
        # self.connect_socket()  # 连接webframe
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)

    # # 创建和webframe交互的套接字
    # def connect_socket(self):
    #     self.connect_sockfd = socket()
    #     frame_addr = (frame_ip,frame_port)
    #     try:
    #         self.connect_sockfd.connect(frame_addr)
    #     except Exception as e:
    #         print(e)
    #         sys.exit()  # 连接异常就退出

    #绑定地址
    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port',self.port)
        while True:
            connfd,addr =self.sockfd.accept()
            print('Connect from',addr)
            client = Thread(target=self.handle,args=(connfd,))
            client.setDaemon(True)
            client.start()

    # 具体处理客户端请求任务
    def handle(self,connfd):
        # 获取http请求
        request = connfd.recv(1096).decode()
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            env = re.match(pattern,request).groupdict()
        except:
            # 客户端断开
            connfd.close()
            return
        else:
            data = connect_frame(env)
            if data:
                self.response(connfd,data)
            # # print(env)
            # # 将字典转换为json
            # data = json.dumps(env)
            # # 将解析后的请求发送给webframe
            # self.connect_sockfd.send(data.encode())
            # # 接收来自webframe数据
            # data = self.connect_sockfd.recv(4096*100).decode()
            # # print(json.loads(data))
            # self.response(connfd,json.loads(data))

    # 给浏览器发送数据
    def response(self,connfd,data):
        # data =>{'status': '200', 'data': 'xxxxxxx'}
        if data['status'] == '200':
            responseHeaders = "HTTP/1.1 200 OK\r\n"  # 响应行
            responseHeaders += "Content-Type:text/html\r\n"  # 响应头
            responseHeaders += "\r\n"  # 换行
            responseBody = data['data']  # 响应体
        elif data['status'] == '404':
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"  # 响应行
            responseHeaders += "Content-Type:text/html\r\n"  # 响应头
            responseHeaders += "\r\n"  # 换行
            responseBody = data['data']  # 响应体
        elif data['status'] == '500':
            pass
        # 给浏览器发送数据
        response_data = responseHeaders+responseBody
        connfd.send(response_data.encode())


httpd = HTTPServer()
httpd.serve_forever()

